#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
__metaclass__ = type

'''
Cisco ACIのスイッチにSSHで接続してiShell上のコマンドshow vpc briefの出力を加工します。
'''
__author__ = 'takamitsu-iida'
__version__ = '0.1'
__date__    = "20210705"

import os
from pathlib import Path
from collections import OrderedDict

#
# FOR ANSIBLE ACTION_PLUGIN
#
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

class ActionModule(ActionBase):

  def run(self, tmp=None, task_vars=None):

    if task_vars is None:
      task_vars = dict()

    result = super(ActionModule, self).run(tmp, task_vars)
    del tmp

    display = Display()

    log_dir = self._task.args.get('log_dir', '')
    file_prefix = self._task.args.get('file_prefix', '')

    working_path = self._loader.get_basedir()
    if self._task._role is not None:
      working_path = self._task._role._role_path

    files = self.get_files(log_dir, file_prefix)
    for f in files:
      display.v(str(f))


    return result

  def get_files(self, dir:str, prefix:str) -> list:
    """ファイル一覧を作成した日付(ctime)の新しい順に取り出す"""
    paths = list(Path(dir).glob('{0}*'.format(prefix)))
    paths.sort(key=os.path.getctime, reverse=True)
    # paths.sort(key=os.path.getmtime, reverse=True)
    return paths



class ShowVpcBriefParser:
    '''show vpc briefコマンドの出力を固定長で切り取ってパースします
    '''

    #
    # クラス変数
    #

    # 処理開始となる行
    start_string = "id   Port   Status Consistency Reason                     Active vlans"

    def __init__(self) -> None:
      pass


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
        k = 'id'
        d[k] = d.get(k, '') + line[0:5].strip()
        k = 'Port'
        d[k] = d.get(k, '') + line[5:12].strip()
        k = 'Status'
        d[k] = d.get(k, '') + line[12:19].strip()
        k = 'Consistency'
        d[k] = d.get(k, '') + line[19:31].strip()
        k = 'Reason'
        d[k] = d.get(k, '') + line[31:58].strip()
        k = 'ActiveVlans'
        d[k] = d.get(k, '') + line[58:].strip()

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
        # 改行コードを含む右端の余白を削除
        line = line.rstrip()

        # 開始行を見つけるまで読み飛ばす
        if line.startswith(ShowVpcBriefParser.start_string):
          is_started = True
          continue

        if not is_started:
          continue

        # 読み飛ばす
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


  def debug() -> int:
    filename1 = "show_vpc_brief.1.txt"
    input_path = os.path.join(app_dir, filename1)
    parser = ShowVpcBriefParser()
    results = parser.parse_file(input_path)
    for entry in results:
      print(entry)
    print("")
    return 0


  def get_files(dir:str, prefix:str) -> list:
    """ファイル一覧を作成した日付(ctime)の新しい順に取り出す"""
    paths = list(Path(dir).glob('{0}*'.format(prefix)))
    paths.sort(key=os.path.getctime, reverse=True)
    # paths.sort(key=os.path.getmtime, reverse=True)
    return paths


  def main() -> int:
    """メイン関数

    Returns:
      int -- 正常終了は0、異常時はそれ以外を返却
    """

    # 引数処理
    parser = argparse.ArgumentParser(description='parse show ip route output.')
    parser.add_argument('-d', '--directory', dest='directory', default='.', help='Directory to search log files')
    parser.add_argument('-p', '--prefix', dest='prefix', default='', help='Prefix of log file')
    parser.add_argument('-t', '--textfsm', dest='textfsm', default='', help='Path to textfsm')
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