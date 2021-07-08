#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__metaclass__ = type

'''
Cisco ACIのiShellで実行したshow vpc briefコマンドの出力を加工します。
'''

__author__ = 'takamitsu-iida'
__version__ = '0.1'
__date__ = "20210705"

import os
from pathlib import Path
from collections import OrderedDict


#
# ANSIBLE ACTION_PLUGIN
#
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from ansible.module_utils.common.text.converters import to_text


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):

        # run module
        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp

        display = Display()

        # get task args
        log_dir = self._task.args.get('log_dir', '')
        file_prefix = self._task.args.get('file_prefix', '')

        working_path = self._loader.get_basedir()
        if self._task._role is not None:
            working_path = self._task._role._role_path

        # .txtファイルを作成した日付(ctime)の新しい順に取り出す
        paths = list(Path(log_dir).glob('{0}*.txt'.format(file_prefix)))
        paths.sort(key=os.path.getctime, reverse=True)
        # paths.sort(key=os.path.getmtime, reverse=True)

        # limit 5 files
        paths = paths[:5]

        display.v("files to be parsed")
        for path in paths:
            display.v("  " + to_text(path))

        # list of filenames
        filenames = []
        for path in paths:
            filenames.append(os.path.basename(path))

        d = OrderedDict()
        parser = ShowVpcBriefParser()
        for path in paths:
            filename = os.path.basename(path)
            parsed_list = parser.parse_file(path)
            if parsed_list:
                d[filename] = parsed_list

        # 先頭の分析結果を取り出す
        first_parsed = next(iter(d.values()))

        # idごとのリストにする
        # 先頭が新しいファイルの情報
        # [ {id: xxx}, {id: xxx}, {id: xxx}]
        result_list = []
        for item in first_parsed:
            port_id = item.get("id")
            port_list = self.get_port_list(d, port_id)
            result_list.append(port_list)

        result['filenames'] = filenames
        result['result_list'] = result_list

        return result


    def get_port_list(self, ordered_dict, port_id):
        result = []
        for filename, parsed_list in ordered_dict.items():
            for item in parsed_list:
                if port_id == item.get("id"):
                    item['filename'] = filename
                    result.append(item)
                    continue
        return result


class ShowVpcBriefParser:
    '''show vpc briefコマンドの出力を固定長で切り取ってパースします
    '''
    #
    # クラス変数
    #

    # 処理開始となる行
    start_string = "id   Port   Status Consistency Reason                     Active vlans"

    def parse_buffers(self, lines):
        """複数行の塊をパースする
        1         2          3        4         5         6         7         8
        012345678901234567890123456789012345678901234567890123456789012345678901234567890
        ----------+---------+----------+--------+---------+---------+---------+---------+
        vPC status
        ----------------------------------------------------------------------
        id   Port   Status Consistency Reason                     Active vlans
        --   ----   ------ ----------- ------                     ------------
        1    Po40   up     success     success                    101-106,109
                                                                ,111
        [0:5][5:12] [12:19][19:31]     [31:58]                    [58:]
        """

        if not lines:
            return None
        d = OrderedDict()
        for line in lines:
            if len(line) < 58:
                continue
            d['id'] = d.get('id', '') + line[0:5].strip()
            d['Port'] = d.get('Port', '') + line[5:12].strip()
            d['Status'] = d.get('Status', '') + line[12:19].strip()
            d['Consistency'] = d.get('Consistency', '') + line[19:31].strip()
            d['Reason'] = d.get('Reason', '') + line[31:58].strip()
            d['ActiveVlans'] = d.get('ActiveVlans', '') + line[58:].strip()

        if len(d) == 0:
            return None
        return d


    def parse_file(self, filename):
        lines = []
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except Exception:
            return []
        return self.parse_lines(lines)


    def parse_lines(self, lines):
        results = []

        # 複数行表示の塊
        buffer_lines = []

        # 処理対象の先頭を見つけたか
        is_started = False

        for line in lines:
            # 開始行を見つけるまで読み飛ばす
            if line.startswith(ShowVpcBriefParser.start_string):
                is_started = True
                continue

            if not is_started:
                continue

            # --で始まっている行は読み飛ばす
            if len(line) == 0 or line.startswith("--"):
                continue

            # 数字で始まっていれば塊を発見
            if line[0].isdigit():
                # 古い塊をパース
                data = self.parse_buffers(buffer_lines)
                if data:
                    results.append(data)
                # バッファを新しくする
                buffer_lines = []
                buffer_lines.append(line)
                continue

            # 空白で始まっていれば塊の一部
            if line[0].isspace():
                buffer_lines.append(line)

        # 最後の塊
        data = self.parse_buffers(buffer_lines)
        if data:
            results.append(data)

        return results


if __name__ == "__main__":

    from pathlib import Path
    import argparse
    import sys


    def here(path=''):
        """相対パスを絶対パスに変換して返却します"""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

    # アプリケーションのホームディレクトリ
    app_dir = here(".")


    def get_files(dir: str, prefix: str) -> list:
        """ファイル一覧を作成した日付(ctime)の新しい順に取り出す"""
        paths = list(Path(dir).glob('{0}*'.format(prefix)))
        paths.sort(key=os.path.getctime, reverse=True)
        # paths.sort(key=os.path.getmtime, reverse=True)
        return paths


    def debug() -> int:
        filename1 = "show_vpc_brief.1.txt"
        input_path = os.path.join(app_dir, filename1)
        parser = ShowVpcBriefParser()
        results = parser.parse_file(input_path)
        for entry in results:
            print(entry)
        print("")
        return 0


    def main() -> int:
        """メイン関数
        Returns:
        int -- 正常終了は0、異常時はそれ以外を返却
        """

        # 引数処理
        parser = argparse.ArgumentParser(description='parse show ip route output.')
        parser.add_argument('-d', '--directory', dest='directory', default='.', help='Directory to search log files')
        parser.add_argument('-p', '--prefix', dest='prefix', default='', help='Prefix of log file')
        parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output')
        parser.add_argument('--debug', action='store_true', default=False, help='Debug to develop script')
        args = parser.parse_args()

        if args.debug:
            return debug()

        if args.directory and args.prefix:
            d = OrderedDict()
            files = get_files(dir=args.directory, prefix=args.prefix)
            # max 10 files
            files = files[:10]
            parser = ShowVpcBriefParser()
            for f in files:
                filename = os.path.basename(f)
                result_list = parser.parse_file(f)
                if result_list:
                    d[filename] = result_list
                print(d)

        return 0

    sys.exit(main())
