#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Ciscoのshow ip routeをパースします

2016/04/20 初版
2021/06/28 textfsmを使ってパースするクラスを追加
"""

__author__ = 'Takamitsu IIDA'
__version__ = '0.2'
__date__ = '2021/06/28'


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
  """IPv4経路を格納する入れ物です"""

  def __init__(self, proto='', ptype='', addr='', mask=-1, gw='', intf=''):
    """コンストラクタ"""
    self.proto = proto
    self.ptype = ptype
    self.addr = addr
    self.mask = mask
    self.gw = gw
    self.intf = intf

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
      return all([self.proto == other.proto, self.addr == other.addr, self.mask == other.mask, self.gw == other.gw])
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
    return '{0} {1}/{2} via {3} {4}'.format((self.proto + ' ' + self.ptype).ljust(12, ' '), self.addr.ljust(16, ' '), str(self.mask).ljust(4, ' '), self.gw.ljust(16, ' '), self.intf)


  def __str__(self):
    """print"""
    return self.__repr__()


  #
  # 以下、フィルタのためのスタティックメソッド
  #
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
  def filter_gw(query:str) -> typing.Callable:
    """ゲートウェイを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.gw):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_interface(query:str) -> typing.Callable:
    """インタフェース名が条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query, re.IGNORECASE)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.intf):
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
    self.pstat = {}
    self.mstat = {}
    self.gstat = {}


  def setCounter(self, d, k) -> None:
    """辞書型dのキーkの値を+1する"""
    if not k:
      return
    counter = d.get(k, 0)
    counter += 1
    d[k] = counter


  def print_statistics(self) -> None:
    """統計情報をprintする"""
    def print_dict(d, key, ljust):
      value = d.get(key)
      if not value:
        return
      if not isinstance(value, str):
        value = str(value)
      print(key.ljust(ljust) + " : " + value)

    for key in self.pstat.keys():
      print_dict(self.pstat, key, 2)
    print("")

    for key in sorted(self.mstat.keys()):
      print_dict(self.mstat, key, 2)
    print("")

    for key in sorted(self.gstat.keys()):
      print_dict(self.gstat, key, 16)


class RegexpRouteParser(RouteParser):
  """Ciscoのshow ip routeコマンド表示を受け取って、加工します"""

  # 正規表現のパターン定義

  # 10.1.22.0
  # _ipv4_addr = r'^(?P<addr>(?:\d{1,3}\.){3}\d{1,3})'

  # 10.1.22.0/24
  # _ipv4_prefix = r'^(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2})'

  #      100.0.0.0/16 is subnetted, 63 subnets
  FIXED_MASK = r'^\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is subnetted'

  #      110.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
  VARIABLE_MASK = r'^\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is variably subnetted'

  # C       192.168.254.1 is directly connected, Loopback0
  FIXED_DIRECTLY_CONNECTED = r'^(?P<proto>\w)\*?\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3}) is directly connected,\s+(?P<interface>\w.*)'

  # S        110.0.0.0/8 is directly connected, Null0
  VARIABLE_DIRECTLY_CONNECTED = r'^(?P<proto>\w)\*?\s+(?P<ptype>\w{0,2})\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is directly connected,\s+(?P<interface>\w.*)'

  # O E1     100.3.0.0 [110/122] via 10.245.2.2, 7w0d, Vlan102
  # S       172.18.0.0 [1/0] via 192.168.1.10
  IPv4_FIXED_PREFIX = r'^(?P<proto>\w)\*?\s(?P<ptype>\w{0,2})\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3}) \[\d+/\d+] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3})(, \w+,\s+(?P<interface>\w.*))?'

  # S*    0.0.0.0/0 [252/0] via 10.245.2.2, Vlan102
  # O        10.244.1.0/24 [110/2] via 10.245.11.2, 7w0d, Vlan111
  # S        10.128.0.0/24 [1/0] via 10.245.29.4, Vlan129
  IPv4_VARIABLE_PREFIX = r'^(?P<proto>\w)\*?\s(?P<ptype>\w{0,2})\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) \[\d+/\d+\] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3})(, \w+)?,\s+(?P<interface>\w.*)$'

  # O    192.168.23.0/24 [110/2] via 192.168.13.3, 7w0d, Vlan13
  #                      [110/2] via 192.168.12.2, 7w0d, Vlan12
  IPv4_PREFIX_ECMP = r'^\*?\s+\[\d+/\d+] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3}), \w+,\s+(?P<interface>\w.*)$'


  def __init__(self) -> None:
    """コンストラクタ"""
    super().__init__()

    # compile regexp
    self.re_fixed_mask = re.compile(RegexpRouteParser.FIXED_MASK)
    self.re_variable_mask = re.compile(RegexpRouteParser.VARIABLE_MASK)
    self.re_fixed_directly_connected = re.compile(RegexpRouteParser.FIXED_DIRECTLY_CONNECTED)
    self.re_variable_directly_connected = re.compile(RegexpRouteParser.VARIABLE_DIRECTLY_CONNECTED)
    self.re_ipv4_fixed_prefix = re.compile(RegexpRouteParser.IPv4_FIXED_PREFIX)
    self.re_ipv4_variable_prefix = re.compile(RegexpRouteParser.IPv4_VARIABLE_PREFIX)
    self.re_ipv4_prefix_ecmp = re.compile(RegexpRouteParser.IPv4_PREFIX_ECMP)


  def get_lines(self, path:str) -> list:
    """ファイルを読んで行配列を返却する"""
    lines = []
    with open(path, 'r') as f:
      for line in f:
        lines.append(line.rstrip())
    return lines


  def parse_file(self, file_path:str) -> list:
    lines = self.get_lines(file_path)

    # リストに格納する
    route_entries = []
    for ipv4_route_entry, line in self.parse_lines(lines):
      route_entries.append(ipv4_route_entry)

    return route_entries


  def parse_lines(self, lines:list) -> typing.Generator[IPv4RouteEntry, None, None]:
    """行の配列を走査してIPv4RouteEntryオブジェクトをyieldする"""
    self.clear_stats()

    current_proto = None
    current_ptype = None
    current_mask = None
    current_addr = None

    for line in lines:
      #       106.0.0.0/16 is subnetted, 7 subnets
      # _fixed_mask = r'\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is subnetted'
      match = re.search(self.re_fixed_mask, line)
      if match:
        current_addr = match.group('addr')
        current_mask = match.group('mask')
        continue

      #       110.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
      # _variable_mask = r'^(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is variably subnetted'
      match = re.search(self.re_variable_mask, line)
      if match:
        continue

      # C       192.168.254.1 is directly connected, Loopback0
      # _fixed_directly_connected = r'^(?P<proto>\w)\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3}) is directly connected,(?P<interface>.*)'
      match = re.match(self.re_fixed_directly_connected, line)
      if match:
        p = match.group('proto')
        a = match.group('addr')
        m = 32
        g = ""
        i = match.group('interface')
        ipv4_route_entry = IPv4RouteEntry(proto=p, addr=a, mask=m, gw=g, intf=i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue

      # S        110.0.0.0/8 is directly connected, Null0
      # _variable_directly_connected = r'^(?P<proto>\w)\s+(?P<ptype>\w{0,2})\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is directly connected,(?P<interface>.*)'
      match = re.match(self.re_variable_directly_connected, line)
      if match:
        p = match.group('proto')
        a = match.group('addr')
        m = match.group('mask')
        g = ""
        i = match.group('interface')
        ipv4_route_entry = IPv4RouteEntry(proto=p, addr=a, mask=m, gw=g, intf=i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue

      # O        10.244.1.0/24 [110/2] via 10.245.11.2, 7w0d, Vlan111
      # _ipv4_variable_prefix = r'^(?P<proto>\w)\s(?P<ptype>\w{0,2})\s+(?P<ptype>\w{0,2})\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) \[\d+/\d+\] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3}),.*,(?P<interface>.*)'
      match = re.match(self.re_ipv4_variable_prefix, line)
      if match:
        p = match.group('proto')
        t = match.group('ptype')
        a = match.group('addr')
        m = match.group('mask')
        g = match.group('gw')
        i = match.group('interface')
        # for in case of ecmp
        current_proto = p
        current_ptype = t
        current_addr = a
        current_mask = m
        ipv4_route_entry = IPv4RouteEntry(proto=p, ptype=t, addr=a, mask=m, gw=g, intf=i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue

      # _ipv4_fixed_prefix = r'^(?P<proto>\w)\s(?P<ptype>\w{0,2})\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3}) \[\d+/\d+] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3}),.*,(?P<interface>.*)'
      match = re.match(self.re_ipv4_fixed_prefix, line)
      if match:
        current_addr = match.group('addr')
        p = match.group('proto')
        t = match.group('ptype')
        a = match.group('addr')
        m = current_mask
        g = match.group('gw')
        i = match.group('interface')
        # for in case of ecmp
        current_proto = p
        current_ptype = t
        current_addr = a
        ipv4_route_entry = IPv4RouteEntry(proto=p, ptype=t, addr=a, mask=m, gw=g, intf=i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue

      # _ipv4_prefix_ecmp = r'^\s+\[\d+/\d+] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3}),.*,(?P<interface>.*)'
      match = re.match(self.re_ipv4_prefix_ecmp, line)
      if match:
        p = current_proto
        t = current_ptype
        a = current_addr
        m = current_mask
        g = match.group('gw')
        i = match.group('interface')
        ipv4_route_entry = IPv4RouteEntry(proto=p, ptype=t, addr=a, mask=m, gw=g, intf=i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue
    # end for


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

    p_index = header.index('PROTOCOL')
    t_index = header.index('TYPE')
    a_index = header.index('NETWORK')
    m_index = header.index('MASK')
    g_index = header.index('NEXTHOP_IP')
    i_index = header.index('NEXTHOP_IF')

    route_entries = []
    for item in parsed_list:
      p = item[p_index].strip()
      t = item[t_index].strip()
      a = item[a_index].strip()
      m = item[m_index].strip()
      g = item[g_index].strip()
      i = item[i_index].strip()
      self.setCounter(self.pstat, p)
      self.setCounter(self.mstat, m)
      self.setCounter(self.gstat, g)
      entry = IPv4RouteEntry(proto=p, ptype=t, addr=a, mask=m, gw=g, intf=i)
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

    # カレントディレクトリからのパス
    input_path = os.path.join(app_dir, filename)

    # 正規表現でパース
    r_parser = RegexpRouteParser()
    r_route_entries = r_parser.parse_file(input_path)
    print("{} routes parsed using RegexpRouteParser".format(len(r_route_entries)))

    # textfsmでパース
    t_parser = TextfsmRouteParser(textfsm_path=os.path.join('cisco_ios_show_ip_route.textfsm'))
    t_route_entries = t_parser.parse_file(input_path)
    print("{} routes parsed using TextfsmRouteParser".format(len(t_route_entries)))

    # 差分を確認
    diff_list = IPv4RouteEntry.get_diff_list(r_route_entries, t_route_entries)
    print("{} routes differ".format(str(len(diff_list))))

    for item in diff_list:
      print(item)


  def test_filter(filename:str) -> None:
    """フィルタのテスト"""

    # カレントディレクトリからのパス
    input_path = os.path.join(app_dir, filename)

    # パーサーをインスタンス化してパース
    parser = RegexpRouteParser()
    route_entries = parser.parse_file(input_path)

    f1 = IPv4RouteEntry.filter_addr(r'^10\.')       # 10.x.x.xで始まるIPアドレス
    f2 = IPv4RouteEntry.filter_mask(24, 'ge')       # マスク長が24ビット以上
    # f3 = IPv4RouteEntry.filter_proto('L')
    # f4 = IPv4RouteEntry.filter_gw('10.245.2.2')
    f5 = IPv4RouteEntry.filter_interface('vlan102') # インタフェースがvlan102
    funcs = [f1, f2, f5]
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
    parser = RegexpRouteParser()
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
    r_parser = RegexpRouteParser()
    t_parser = TextfsmRouteParser(textfsm_path=os.path.join(app_dir, 'cisco_ios_show_ip_route.textfsm'))
    r_parser.parse_file(input_path)
    t_parser.parse_file(input_path)

    # 統計情報を表示
    print("parsed by RegexpRouteParser")
    r_parser.print_statistics()
    print("")
    print("parsed by TextfsmRouteParser")
    t_parser.print_statistics()


  def test_textfsm(filename:str) -> None:
    """textfsmによるパース"""
    if not HAS_TEXTFSM:
      return 1

    input_path = os.path.join(app_dir, filename)
    textfsm_path = os.path.join(app_dir, 'cisco_ios_show_ip_route.textfsm')
    parser = TextfsmRouteParser(textfsm_path)
    route_entries = parser.parse_file(input_path)
    for entry in route_entries:
      print(entry)


  def debug() -> None:
    filename1 = "show_ip_route1.log"
    filename2 = "show_ip_route2.log"
    filename3 = "show_ip_route3.log"  # ECMP経路あり
    test_parse(filename1)
    # test_parse(filename2)
    # test_parse(filename3)
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
      textfsm_path = args.textfsm if args.textfsm else os.path.join(app_dir, 'cisco_ios_show_ip_route.textfsm')
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