#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Cisco ACIのスイッチにSSH接続してshow ip route vrf allを実行し、結果をパースします

2016/07/03 初版
"""

__author__ = 'Takamitsu IIDA'
__version__ = '0.1'
__date__ = '2021/07/03'


#
# 標準ライブラリのインポート
#
import re
import os
import sys
from typing import Text
import typing

#
# 外部ライブラリのインポート
#
HAS_TEXTFSM = True
try:
  import textfsm
except ImportError:
  HAS_TEXTFSM = False


def here(path=''):
  """相対パスを絶対パスに変換して返却します"""
  return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

# アプリケーションのホームディレクトリ
app_dir = here(".")

# filesのディレクトリ
files_dir = here("../files")


class IPv4RouteEntry:
  """IPv4経路を格納する入れ物です

  textfsmでパースした際のヘッダ項目は以下の通り
    VRF
    NETWORK
    MASK
    NEXTHOP_IP
    NEXTHOP_IF
    UPTIME
    PROTOCOL
    TYPE
  """

  def __init__(self, vrf='', addr='', mask=-1, gw_ip='', gw_if='', proto='', ptype=''):
    """コンストラクタ"""
    self.vrf = vrf
    self.addr = addr
    self.mask = mask
    self.gw_ip = gw_ip
    self.gw_if = gw_if
    self.proto = proto
    self.ptype = ptype

    # change mask str to int
    try:
      if isinstance(self.mask, str):
        self.mask = int(mask)
    except Exception:
      raise ValueError('mask error')

    # add addr32
    try:
      cols = addr.split('.')
      self.addr32 = int(cols[0]) * 256 * 256 * 256 + int(cols[1]) * 256 * 256 + int(cols[2] * 256) + int(cols[3])
    except Exception:
      self.addr32 = -1
      # raise ValueError('address error')


  def __eq__(self, other):
    """=="""
    if isinstance(other, self.__class__):
      return all([
        self.vrf == other.vrf,
        self.addr == other.addr,
        self.mask == other.mask,
        self.gw_ip == other.gw_ip,
        self.gw_if == other.gw_if,
        self.proto == other.proto,
        self.ptype == other.ptype
      ])
    return False


  def __lt__(self, other):
    """less than"""
    return self.addr32 < other.addr32


  def __gt__(self, other):
    """greater than"""
    return self.addr32 > other.addr32


  def __le__(self, other):
    """less or equal"""
    return self.addr32 <= other.addr32


  def __ge__(self, other):
    """greater or equal"""
    return self.addr32 >= other.addr32


  def __repr__(self):
    """print"""
    return '{0} {1} /{2} via {3} {4} {5}'.format(self.vrf.ljust(30), self.addr.ljust(16, ' '), str(self.mask).ljust(4, ' '),  self.gw_ip.ljust(16, ' '), self.gw_if.ljust(12, ' '), self.proto.ljust(12), self.ptype)

  def __str__(self):
    """print"""
    return self.__repr__()


  #
  # 以下、フィルタのためのスタティックメソッド
  #

  @staticmethod
  def filter_vrf(query:str) -> typing.Callable:
    """vrfを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.vrf):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_addr(query:str) -> typing.Callable:
    """アドレスを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.addr):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_proto(query:str) -> typing.Callable:
    """プロトコルを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query, re.IGNORECASE)

    def _filter(ipv4_route_entry) -> function:
      ret = None
      if r.search(ipv4_route_entry.proto):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_gw_ip(query:str) -> typing.Callable:
    """ゲートウェイを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.gw_ip):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_gw_if(query:str) -> typing.Callable:
    """インタフェース名が条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query, re.IGNORECASE)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.gw_if):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_mask(masklen:int, *_ope:str) -> typing.Callable:
    """マスク長が条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    if _ope:
      ope = _ope[0]
    else:
      ope = 'eq'

    def _filter(ipv4_route_entry):
      ret = None
      if ope == 'le':
        if ipv4_route_entry.mask <= masklen:
          ret = ipv4_route_entry
      if ope == 'lt':
        if ipv4_route_entry.mask < masklen:
          ret = ipv4_route_entry
      if ope == 'ge':
        if ipv4_route_entry.mask >= masklen:
          ret = ipv4_route_entry
      if ope == 'gt':
        if ipv4_route_entry.mask > masklen:
          ret = ipv4_route_entry
      if ope == 'eq':
        if ipv4_route_entry.mask == masklen:
          ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def get_filter_result(ipv4_route_entry, funcs:list):
    """IPv4RouteEntryとフィルタ関数の配列を受け取り、フィルタの条件にあえばそのIPv4RouteEntryを返却する"""
    func = funcs[0]
    result = func(ipv4_route_entry)
    if result and funcs[1:]:
      return IPv4RouteEntry.get_filter_result(ipv4_route_entry, funcs[1:])
    return result, func


  @staticmethod
  def get_diff_list(src_list:list, dst_list:list) -> list:
    """差分を取り、追加は['+', ipv4_route_entry]、削除は['-', ipv4_route_entry]で返却します"""
    plus =  [['+', entry] for entry in src_list if entry not in dst_list]
    minus = [['-', entry] for entry in dst_list if entry not in src_list]
    return plus + minus


  @staticmethod
  def get_diff_text(diff_list:list) -> str:
    """差分のリストをテキストにして返却します"""
    if not diff_list:
      return "差分なし"
    text = ""
    for l in diff_list:
      text += l[0].ljust(3) + l[1].toString() + "\n"
    return text


  @staticmethod
  def get_diff_csv(diff_list:list) -> str:
    """差分のリストをCSVテキストにして返却します"""
    text = "ope, ipv4 route entry\n"
    if not diff_list:
      text += "=,no difference\n"
      return text
    for l in diff_list:
      text += l[0] + "," + l[1].toString() + "\n"
    return text


class RouteParser:
  """ルーティングテーブルをパースするベースクラス"""

  def __init__(self) -> None:
    self.clear_stats()


  def clear_stats(self) -> None:
    self.vrf_dict = {}


  def get_vrf_dict(self, vrf) -> dict:
    """vrf名に対応した辞書を返却"""
    vrf_dict = self.vrf_dict.get(vrf, None)
    if vrf_dict is None:
      self.vrf_dict[vrf] = vrf_dict = {}
    return vrf_dict


  def get_dict(self, vrf, dict_key):
    """vrf名に対応した辞書からキーkに対応する辞書を返却"""
    vrf_dict = self.get_vrf_dict(vrf)
    d = vrf_dict.get(dict_key, None)
    if d is None:
      vrf_dict[dict_key] = d = {}
    return d


  def setCounter(self, vrf, dict_key, k) -> None:
    """vrfに対応する辞書型からキーdに対応する辞書を取り出し、そのキーkの値を+1する"""
    if not k:
      return
    d = self.get_dict(vrf, dict_key)
    counter = d.get(k, 0)
    counter += 1
    d[k] = counter


  def print_statistics(self) -> None:
    """統計情報をprintする"""

    def print_dict(d, key, ljust):
      value = d.get(key, None)
      if value is None:
        return
      if not isinstance(value, str):
        value = str(value)
      print(key.ljust(ljust) + " : " + value)

    for vrf in self.vrf_dict.keys():
      pstat = self.get_dict(vrf, 'p')
      mstat = self.get_dict(vrf, 'm')
      gstat = self.get_dict(vrf, 'g')

      print('='*len(vrf))
      print(vrf)
      print('='*len(vrf))

      print("protocol stats")
      for key in pstat.keys():
        print_dict(pstat, key, 2)
      print("")

      print("mask stats")
      for key in sorted(mstat.keys()):
        print_dict(mstat, key, 2)
      print("")

      print("prefix stats per gateway ip")
      for key in sorted(gstat.keys()):
        print_dict(gstat, key, 16)
      print("")


class TextfsmRouteParser(RouteParser):
  """Parse using textfsm"""

  def __init__(self, textfsm_path) -> None:
    """コンストラクタ"""
    super().__init__()
    if not HAS_TEXTFSM:
      raise ValueError('textfsm not imported')
    self.textfsm_path = textfsm_path


  def parse_file(self, file_path:str) -> list:
    """parse file using textfsm"""
    try:
      with open(self.textfsm_path) as f:
        table = textfsm.TextFSM(f)
    except FileNotFoundError:
      raise ValueError("{0} not found".format(self.textfsm_path))

    try:
      with open(file_path, 'r') as f:
        data = f.read()
    except FileNotFoundError:
      print("{0} not found".format(file_path))
      return None

    self.clear_stats()

    header = table.header
    parsed_list = table.ParseText(data)

    v_index = header.index('VRF')
    a_index = header.index('NETWORK')
    m_index = header.index('MASK')
    g_index = header.index('NEXTHOP_IP')
    i_index = header.index('NEXTHOP_IF')
    p_index = header.index('PROTOCOL')
    t_index = header.index('TYPE')

    route_entries = []
    for item in parsed_list:
      v = item[v_index].strip()
      a = item[a_index].strip()
      m = item[m_index].strip()
      g = item[g_index].strip()
      i = item[i_index].strip()
      p = item[p_index].strip()
      t = item[t_index].strip()
      self.setCounter(v, 'p', p)
      self.setCounter(v, 'm', m)
      self.setCounter(v, 'g', g)
      entry = IPv4RouteEntry(vrf=v, addr=a, mask=m, gw_ip=g, gw_if=i, proto=p, ptype=t)
      route_entries.append(entry)

    return route_entries


if __name__ == "__main__":

  # python -m doctest show_ip_route.py

  from pathlib import Path
  import argparse


  def get_files(dir:str, prefix:str) -> list:
    paths = list(Path(dir).glob('{0}*'.format(prefix)))
    paths.sort(key=os.path.getctime, reverse=True)
    # paths.sort(key=os.path.getmtime, reverse=True)
    return paths


  def test_parse(filename:str) -> None:
    """ファイルから経路をパースする"""
    if not HAS_TEXTFSM:
      return 1

    input_path = os.path.join(app_dir, filename)
    parser = TextfsmRouteParser(textfsm_path=os.path.join('aci_show_ip_route_vrf_all.textfsm'))
    route_entries = parser.parse_file(input_path)
    for entry in route_entries:
      print(entry)
    print("")
    print("{} routes parsed using TextfsmRouteParser".format(len(route_entries)))


  def test_filter(filename:str) -> None:
    """フィルタのテスト"""

    # カレントディレクトリからのパス
    input_path = os.path.join(app_dir, filename)

    # パーサーをインスタンス化してパース
    parser = TextfsmRouteParser(textfsm_path=os.path.join('aci_show_ip_route_vrf_all.textfsm'))
    route_entries = parser.parse_file(input_path)

    f1 = IPv4RouteEntry.filter_addr(r'^10\.')       # 10.x.x.xで始まるIPアドレス
    f2 = IPv4RouteEntry.filter_mask(29, 'gt')       # マスク長が29ビットより大きい
    f3 = IPv4RouteEntry.filter_gw_if(r'eth1/.*') # インタフェースがvlan102
    # f4 = IPv4RouteEntry.filter_gw('10.245.2.2')
    # f3 = IPv4RouteEntry.filter_proto('L')
    f4 = IPv4RouteEntry.filter_vrf(r'K5_2n.*')

    # funcs = [f1, f2, f3]
    funcs = [f4]
    for ipv4_route_entry in route_entries:
      result, func = IPv4RouteEntry.get_filter_result(ipv4_route_entry, funcs)
      if result:
        print(result)


  def test_diff(filename1:str, filename2:str) -> None:
    """差分を取るテスト"""

    # カレントディレクトリからのパス
    input_path1 = os.path.join(app_dir, filename1)
    input_path2 = os.path.join(app_dir, filename2)

    # パーサーをインスタンス化してパース
    parser = TextfsmRouteParser(textfsm_path=os.path.join('aci_show_ip_route_vrf_all.textfsm'))
    route_entries1 = parser.parse_file(input_path1)
    route_entries2 = parser.parse_file(input_path2)

    diff_list = IPv4RouteEntry.get_diff_list(route_entries1, route_entries2)
    for diff in diff_list:
      print(diff)


  def test_stat(filename:str) -> None:
    """統計のテスト"""

    # カレントディレクトリからのパス
    input_path = os.path.join(app_dir, filename)

    # パーサーをインスタンス化してパース
    parser = TextfsmRouteParser(textfsm_path=os.path.join(app_dir, 'aci_show_ip_route_vrf_all.textfsm'))
    parser.parse_file(input_path)

    # 統計情報を表示
    print("parsed by TextfsmRouteParser")
    parser.print_statistics()


  def debug() -> None:
    filename1 = "show_ip_route_vrf_all.1.log"
    filename2 = "show_ip_route_vrf_all.2.log"
    test_parse(filename1)
    # test_parse(filename2)
    # test_filter(filename1)
    # test_stat(filename1)
    # test_diff(filename1, filename2)


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
    parser.add_argument('--debug', action='store_true', default=False, help='Debug to develop script')
    args = parser.parse_args()

    if args.debug:
      debug()
      return 0

    if args.directory and args.prefix:
      textfsm_path = args.textfsm if args.textfsm else os.path.join(app_dir, 'aci_show_ip_route_vrf_all.textfsm')
      files = get_files(dir=args.directory, prefix=args.prefix)
      if len(files) >= 2:
        src_path = files[0]
        print("newest file: {}".format(os.path.basename(src_path)))
        parser = TextfsmRouteParser(textfsm_path)
        src_route_entries = parser.parse_file(src_path)
        parser.print_statistics()
        print("")
        # for entry in src_route_entries:
        #   print(entry)
        # print("")

        for i in range(1, len(files)):
          dst_path = files[i]
          dst_route_entries = parser.parse_file(dst_path)

          diff_list = IPv4RouteEntry.get_diff_list(src_route_entries, dst_route_entries)

          flat_diff_list = [i for x in diff_list for i in x]
          num_plus = flat_diff_list.count('+')
          str_plus = str(num_plus).ljust(3)
          num_minus = flat_diff_list.count('-')
          str_minus = str(num_minus).ljust(3)
          num_diff = len(diff_list)
          str_diff = str(num_diff).ljust(3)
          print("diff: {} +: {} -: {}   {}".format(str_diff, str_plus, str_minus, os.path.basename(dst_path)))

    return 0

  sys.exit(main())