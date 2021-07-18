#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__metaclass__ = type

'''
Pythonのdifflibを使ってファイルの差分を返却します
'''
__author__ = 'takamitsu-iida'
__version__ = '0.1'
__date__ = "20210705"


import difflib
import os
from pathlib import Path


#
# ANSIBLE ACTION_PLUGIN
#
from ansible.module_utils.common.text.converters import to_text
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):

        # run module
        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp

        display = Display()

        # get task args
        # tasks/main.yml
        # - name: analyze log
        #   cli_diff:
        #     dst_dir: "{{ LOG_DIR }}"
        #     dst_file_prefix: "{{ inventory_hostname }}"
        #     dst_file_ext: ".txt"
        #   register: r
        dst_dir = self._task.args.get('dst_dir')
        dst_file_prefix = self._task.args.get('dst_file_prefix')
        dst_file_ext = self._task.args.get('dst_file_ext', '.txt')

        # display.v(to_text(self._task.args))

        working_path = self._loader.get_basedir()
        if self._task._role is not None:
            working_path = self._task._role._role_path

        # .txtファイルを作成した日付(ctime)の新しい順に取り出す
        paths = list(Path(dst_dir).glob('{0}*{1}'.format(dst_file_prefix, dst_file_ext)))
        if not paths and len(paths) == 0:
            result['failed'] = True
            result['msg'] = "file not found"
            return result

        paths.sort(key=os.path.getctime, reverse=True)
        # paths.sort(key=os.path.getmtime, reverse=True)

        # limit 5 files
        paths = paths[:5]

        display.v("files to be parsed")
        for path in paths:
            display.v("  " + to_text(path))

        # pickup the newest file as from file
        from_path = paths[0]
        from_file = os.path.basename(from_path)
        from_lines = self.read_lines(from_path)
        if from_lines is None:
            result['failed'] = True
            result['msg'] = "failed to read file {}".format(from_path)
            return result

        df = difflib.HtmlDiff()
        diff_list = []
        for to_path in paths:
            to_file = os.path.basename(to_path)
            if to_path == from_path:
                continue
            to_lines = self.read_lines(to_path)
            if to_lines is None:
                continue

            d = {}
            d['from_path'] = to_text(from_path)
            d['from_file'] = to_text(from_file)
            d['to_path'] = to_text(to_path)
            d['to_file'] = to_text(to_file)
            d['diff'] =  df.make_table(from_lines, to_lines, fromdesc=from_file, todesc=to_file, context=False)
            diff_list.append(d)

        result['diff_list'] = diff_list
        return result


    def read_lines(self, path: str) -> list:
        try:
            with open(path) as f:
                return f.readlines()
        except Exception:
            pass
        return None


    def get_files(self, dir: str, prefix: str, ext=".txt") -> list:
        """ファイル一覧を作成した日付(ctime)の新しい順に取り出す"""
        paths = list(Path(dir).glob('{0}*{1}'.format(prefix, ext)))
        paths.sort(key=os.path.getctime, reverse=True)
        # paths.sort(key=os.path.getmtime, reverse=True)
        return paths




if __name__ == "__main__":

    import argparse
    import sys
    from pathlib import Path


    def here(path=''):
        """相対パスを絶対パスに変換して返却します"""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

    # アプリケーションのホームディレクトリ
    app_dir = here(".")


    def read_lines(path: str) -> list:
        try:
            with open(path) as f:
                return f.readlines()
        except Exception:
            pass
        return None


    def get_files(dir: str, prefix: str, ext=".txt") -> list:
        """ファイル一覧を作成した日付(ctime)の新しい順に取り出す"""
        paths = list(Path(dir).glob('{0}*{1}'.format(prefix, ext)))
        paths.sort(key=os.path.getctime, reverse=True)
        # paths.sort(key=os.path.getmtime, reverse=True)
        return paths


    def main() -> int:
        """メイン関数
        Returns:
        int -- 正常終了は0、異常時はそれ以外を返却
        """

        # 引数処理
        parser = argparse.ArgumentParser(description='generate diff html.')
        parser.add_argument('-d', '--directory', dest='directory', default='.', help='Directory to search log files')
        parser.add_argument('-p', '--prefix', dest='prefix', default='', help='Prefix of log file')
        parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output')
        args = parser.parse_args()

        if args.directory and args.prefix:
            files = get_files(dir=args.directory, prefix=args.prefix)
            # max 5 files
            files = files[:5]
            from_path = files[0]
            from_file = os.path.basename(from_path)
            from_lines = read_lines(from_path)
            result_list = []
            df = difflib.HtmlDiff()
            for to_path in files:
                if to_path == from_path:
                    continue
                to_file = os.path.basename(to_path)
                to_lines = read_lines(to_path)
                if from_lines is None or to_lines is None:
                    continue
                d = {}
                d['from_path'] = from_path
                d['from_file'] = from_file
                d['to_path'] = to_path
                d['to_file'] = to_file
                d['diff'] =  df.make_table(from_lines, to_lines, context=True)
                result_list.append(d)
            print(result_list)
        return 0

    sys.exit(main())
