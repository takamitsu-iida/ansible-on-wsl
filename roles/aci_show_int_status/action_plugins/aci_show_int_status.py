#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__metaclass__ = type

'''
Cisco ACIのスイッチのiShellで実行したshow int statusコマンドの出力を加工します。
'''
__author__ = 'takamitsu-iida'
__version__ = '0.1'
__date__ = "20210705"


import os
from collections import OrderedDict
from io import StringIO
from pathlib import Path

#
# textfsm is required
#
try:
    from textfsm import TextFSM
    HAS_TEXTFSM = True
except ImportError as e:
    HAS_TEXTFSM = False

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
        parser = ShowIntStatusParser()
        for path in paths:
            parsed_list = parser.parse_file(path)
            if parsed_list:
                filename = os.path.basename(path)
                d[filename] = parsed_list

        # 先頭の分析結果を取り出す
        first_parsed = next(iter(d.values()))

        # Portごとのリストに変換する
        # 先頭が新しいファイルの情報
        # [ {Port: xxx}, {Port: xxx}, {Port: xxx}]
        result_list = []
        for item in first_parsed:
            port_id = item.get('Port')
            port_list = self.get_port_list(d, port_id)
            result_list.append(port_list)

        result['filenames'] = filenames
        result['result_list'] = result_list
        return result


    def get_port_list(self, ordered_dict, port_id):
        result = []
        for filename, parsed_list in ordered_dict.items():
            for item in parsed_list:
                if port_id == item.get('Port'):
                    item['filename'] = filename
                    result.append(item)
                    continue
        return result


class ShowIntStatusParser:
    '''show interface statusコマンドの出力をパースします
    '''
    # textfsmのテンプレートは別ファイルにするほどのものでもないので文字列で定義する
    TEMPLATE = """
# ----------------------------------------------------------------------------------------------
#  Port           Name                Status     Vlan       Duplex   Speed    Type
# ----------------------------------------------------------------------------------------------
#  mgmt0          --                  connected  routed     full     1G       --
#  Eth1/1         --                  connected  trunk      full     10G      10g
#  Eth1/2         --                  connected  trunk      full     10G      10g
Value PORT (Eth\d/\d+)
Value STATUS (\S+)
Value DUPLEX (full|auto)
Value SPEED (--|auto|inherit|\d+G)
Value TYPE (\S+)

Start
  ^\s+${PORT}\s+\S+\s+${STATUS}\s+\S+\s+${DUPLEX}\s+${SPEED}\s+${TYPE} -> Record

EOF
    """

    def get_table(self):
        f = StringIO(ShowIntStatusParser.TEMPLATE.strip())
        return TextFSM(f)


    def parse_file(self, input_path) -> list:
        data = None
        try:
            with open(input_path, "r") as f:
                data = f.read()
        except Exception:
            return []

        table = self.get_table()
        parsed_list = table.ParseText(data)

        result_list = []
        # convert list of list to list of dict
        for item in parsed_list:
            d = {
                'Port': item[0],
                'Status': item[1],
                'Duplex': item[2],
                'Speed': item[3],
                'Type': item[4]
            }
            result_list.append(d)

        return result_list


if __name__ == "__main__":

    import argparse
    import sys
    from pathlib import Path


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
        filename1 = "leaf1_show_int_status.1.txt"
        input_path = os.path.join(app_dir, filename1)
        parser = ShowIntStatusParser()
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
            parser = ShowIntStatusParser()
            for f in files:
                filename = os.path.basename(f)
                result_list = parser.parse_file(f)
                if result_list:
                    d[filename] = result_list
                print(d)

        return 0

    sys.exit(main())
