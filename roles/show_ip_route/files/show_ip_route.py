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


class IPv4RouteEntry(object):
  """IPv4経路を格納する入れ物です"""

  proto = None
  addr = None
  mask = None
  gw = None
  interface = None

  def __init__(self, proto, addr, mask, gw, interface):
    """コンストラクタ"""
    self.proto = proto
    self.addr = addr
    try:
      if isinstance(mask, str):
        self.mask = int(mask)
    except Exception:
      raise ValueError('mask error')
    self.gw = gw
    self.interface = interface
    try:
      cols = addr.split('.')
      self.addr32 = int(cols[0]) * 256 * 256 * 256 + int(cols[1]) * 256 * 256 + int(cols[2] * 256) + int(cols[3])
    except Exception:
      raise ValueError('address error')


  def __eq__(self, other):
    """=="""
    return all([self.addr == other.addr, self.mask == other.mask, self.gw == other.gw])


  def __ne__(self, other):
    """!="""
    return not all([self.addr == other.addr, self.mask == other.mask, self.gw == other.gw])


  def __cmp__(self, other):
    """比較"""
    return self.addr32 - other.addr32


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
    return '{0} {1}/{2} via {3} {4}'.format(self.proto, self.addr, self.mask, self.gw, self.interface)


  def __str__(self):
    """print"""
    return self.__repr__()


  #
  # 以下、フィルタのためのスタティックメソッド
  #
  @staticmethod
  def filter_addr(query):
    """アドレスを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.addr):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_proto(query):
    """プロトコルを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query, re.IGNORECASE)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.proto):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_gw(query):
    """ゲートウェイを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.gw):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_interface(query):
    """インタフェース名が条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）"""
    r = re.compile(r"%s" % query, re.IGNORECASE)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.interface):
        ret = ipv4_route_entry
      return ret
    return _filter


  @staticmethod
  def filter_mask(masklen, *_ope):
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
  def get_filter_result(ipv4_route_entry, funcs):
    """IPv4RouteEntryとフィルタ関数の配列を受け取り、フィルタの条件にあえばそのIPv4RouteEntryを返却する"""
    func = funcs[0]
    result = func(ipv4_route_entry)
    if result and funcs[1:]:
      return IPv4RouteEntry.get_filter_result(ipv4_route_entry, funcs[1:])
    return result, func


  @staticmethod
  def get_diff_list(src_list, dst_list):
    """差分を取り、追加は['+', ipv4_route_entry]、削除は['-', ipv4_route_entry]で返却します"""
    plus = [['+', ipv4_route_entry] for ipv4_route_entry in dst_list if ipv4_route_entry not in src_list]
    minus = [['-', ipv4_route_entry] for ipv4_route_entry in src_list if ipv4_route_entry not in dst_list]
    return plus + minus


  @staticmethod
  def get_diff_text(diff_list):
    """差分のリストをテキストにして返却します"""
    if not diff_list:
      return "差分なし"
    text = ""
    for l in diff_list:
      text += l[0].ljust(3) + l[1].toString() + "\n"
    return text


  @staticmethod
  def get_diff_csv(diff_list):
    """差分のリストをCSVテキストにして返却します"""
    text = "ope, ipv4 route entry\n"
    if not diff_list:
      text += "=,no difference\n"
      return text
    for l in diff_list:
      text += l[0] + "," + l[1].toString() + "\n"
    return text



class ShowIpRouteParser(object):
  """Ciscoのshow ip routeコマンド表示を受け取って、加工します"""

  # 正規表現のパターン定義

  # 10.1.22.0
  _ipv4_addr = r'(?P<addr>(?:\d{1,3}\.){3}\d{1,3})'

  # 10.1.22.0/24
  _ipv4_prefix = r'(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2})'

  #      100.0.0.0/16 is subnetted, 63 subnets
  _fixed_mask = r'(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is subnetted'

  #      110.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
  _variable_mask = r'(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is variably subnetted'

  # C       192.168.250.11 is directly connected, Loopback11
  _fixed_directly_connected = r'(?P<proto>.*)\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3}) is directly connected,(?P<interface>.*)'

  # S        110.0.0.0/8 is directly connected, Null0
  _variable_directly_connected = r'(?P<proto>.*)\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is directly connected,(?P<interface>.*)'

  # O E1     100.3.0.0 [110/122] via 10.245.2.2, 7w0d, Vlan102
  _ipv4_fixed_prefix = r'(?P<proto>.*)\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3}) \[\d+/\d+] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3}),.*,(?P<interface>.*)'

  # O        10.244.1.0/24 [110/2] via 10.245.11.2, 7w0d, Vlan111
  _ipv4_variable_prefix = r'(?P<proto>.*)\s+(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) \[\d+/\d+\] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3}),.*,(?P<interface>.*)'

  # O    192.168.23.0/24 [110/2] via 192.168.13.3, 7w0d, Vlan13
  #                      [110/2] via 192.168.12.2, 7w0d, Vlan12
  _ipv4_prefix_ecmp = r'\s+\[\d+/\d+] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3}),.*,(?P<interface>.*)'

  # 統計情報
  pstat = None
  mstat = None
  gstat = None


  def __init__(self):
    """コンストラクタ"""
    self.re_ipv4_addr = re.compile(self._ipv4_addr)
    self.re_ipv4_prefix = re.compile(self._ipv4_prefix)
    self.re_fixed_mask = re.compile(self._fixed_mask)
    self.re_variable_mask = re.compile(self._variable_mask)
    self.re_fixed_directly_connected = re.compile(self._fixed_directly_connected)
    self.re_variable_directly_connected = re.compile(self._variable_directly_connected)
    self.re_ipv4_fixed_prefix = re.compile(self._ipv4_fixed_prefix)
    self.re_ipv4_variable_prefix = re.compile(self._ipv4_variable_prefix)
    self.re_ipv4_prefix_ecmp = re.compile(self._ipv4_prefix_ecmp)
    self.pstat = {}
    self.mstat = {}
    self.gstat = {}


  def setCounter(self, d, k):
    """辞書型dのキーkの値を+1する"""
    if not k:
      return
    counter = d.get(k, 0)
    counter += 1
    d[k] = counter


  def parse_lines(self, lines):
    """行の配列を走査してIPv4RouteEntryオブジェクトをyieldする"""
    current_proto = None
    current_mask = None
    current_addr = None

    for line in lines:

      #       106.0.0.0/16 is subnetted, 7 subnets
      # r'(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is subnetted'
      match = re.search(self.re_fixed_mask, line)
      if match:
        current_addr = match.group('addr')
        current_mask = match.group('mask')
        continue

      #       110.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
      # r'(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) is variably subnetted'
      match = re.search(self.re_variable_mask, line)
      if match:
        continue

      # C       192.168.250.11 is directly connected, Loopback11
      match = re.match(self.re_fixed_directly_connected, line)
      if match:
        p = match.group('proto').strip()
        a = match.group('addr')
        m = current_mask
        g = ""
        i = match.group('interface')
        ipv4_route_entry = IPv4RouteEntry(p, a, m, g, i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue

      # S        110.0.0.0/8 is directly connected, Null0
      # r'(?P<proto>.*)(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2})is directly connected,(?P<interface>.*)'
      match = re.match(self.re_variable_directly_connected, line)
      if match:
        p = match.group('proto').strip()
        a = match.group('addr')
        m = match.group('mask')
        g = ""
        i = match.group('interface')
        ipv4_route_entry = IPv4RouteEntry(p, a, m, g, i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue

      # O        10.244.1.0/24 [110/2] via 10.245.11.2, 7w0d, Vlan111
      # r'(?P<proto>.*)(?P<addr>(?:\d{1,3}\.){3}\d{1,3})/(?P<mask>\d{1,2}) \[\d+/\d+\] via (?P<gw>(?:\d{1,3}\.){3}\d{1,3}),.*,(?P<interface>.*)'
      match = re.match(self.re_ipv4_variable_prefix, line)
      if match:
        p = match.group('proto').strip()
        a = match.group('addr')
        m = match.group('mask')
        g = match.group('gw')
        i = match.group('interface')
        current_proto = p
        current_addr = a
        current_mask = m
        ipv4_route_entry = IPv4RouteEntry(p, a, m, g, i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue

      match = re.match(self.re_ipv4_fixed_prefix, line)
      if match:
        current_addr = match.group('addr')
        p = match.group('proto').strip()
        a = match.group('addr')
        m = current_mask
        g = match.group('gw')
        i = match.group('interface')
        current_proto = p
        current_addr = a
        ipv4_route_entry = IPv4RouteEntry(p, a, m, g, i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue

      match = re.match(self.re_ipv4_prefix_ecmp, line)
      if match:
        p = current_proto
        a = current_addr
        m = current_mask
        g = match.group('gw')
        i = match.group('interface')
        ipv4_route_entry = IPv4RouteEntry(p, a, m, g, i)
        self.setCounter(self.pstat, p)
        self.setCounter(self.mstat, m)
        self.setCounter(self.gstat, g)
        yield ipv4_route_entry, line
        continue
    # end for


  def print_statistics(self):
    """統計情報をprintする"""
    def print_dict(d, key, ljust):
      value = d.get(key)
      if not value:
        return
      if not isinstance(value, str):
        value = str(value)
      print(key.ljust(ljust) + " : " + value)

    for key in self.pstat.keys():
      print_dict(self.pstat, key, 5)
    print("")
    for key in sorted(self.mstat):
      print_dict(self.mstat, key, 2)
    print("")
    for key in sorted(self.gstat):
      print_dict(self.gstat, key, 16)



class ShowIpRouteTextfsm(object):
  """Parse by Textfsm"""

  textfsm_path = None
  table = None


  def __init__(self, textfsm_path):
    """コンストラクタ"""

    self.textfsm_path = textfsm_path
    try:
      with open(textfsm_path) as f:
        self.table = textfsm.TextFSM(f)
    except FileNotFoundError:
      raise ValueError("{0} not found".format(textfsm_path))
    except Exception as e:
      print(e.__class__.__name__)
      raise ValueError('invalid textfsm_path')


  def parse_file(self, file_path):

    try:
      with open(file_path, 'r') as f:
        data = f.read()
    except FileNotFoundError:
      print("{0} not found".format(file_path))
      return None

    route_entries = []

    parsed_list = self.table.ParseText(data)
    for item in parsed_list:
      proto = (item[0] + ' ' + item[1]).strip()
      addr = item[2]
      mask = item[3]
      gw = item[6]
      intf = item[7]
      entry = IPv4RouteEntry(proto=proto, addr=addr, mask=mask, gw=gw, interface=intf)
      route_entries.append(entry)

    return route_entries


if __name__ == "__main__":

  # python -m doctest show_ip_route.py

  def read_file(path):
    """ファイルを読んで行配列を返却する"""
    lines = []
    with open(path, 'r') as f:
      for line in f:
        lines.append(line.rstrip())
    return lines


  def test_parse(filename):
    """ファイルから経路をパースする"""

    # カレントディレクトリからのパス
    input_path = os.path.join(app_dir, filename)

    # ファイルを行配列にする
    lines = read_file(input_path)

    # パーサーをインスタンス化する
    parser = ShowIpRouteParser()

    # リストに格納する
    route_entries = []
    for ipv4_route_entry, line in parser.parse_lines(lines):
      route_entries.append(ipv4_route_entry)

    for ipv4_route_entry in route_entries:
      print(ipv4_route_entry)


  def test_filter(filename):
    """フィルタのテスト"""

    # カレントディレクトリからのパス
    input_path = os.path.join(app_dir, filename)

    # ファイルを行配列にする
    lines = read_file(input_path)

    # パーサーをインスタンス化する
    parser = ShowIpRouteParser()

    # リストに格納する
    route_entries = []
    for ipv4_route_entry, line in parser.parse_lines(lines):
      route_entries.append(ipv4_route_entry)

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


  def test_diff(filename1, filename2):
    """差分を取るテスト"""

    # カレントディレクトリからのパス
    input_path1 = os.path.join(app_dir, filename1)
    input_path2 = os.path.join(app_dir, filename2)

    lines1 = read_file(input_path1)
    lines2 = read_file(input_path2)

    # パーサーをインスタンス化する
    parser = ShowIpRouteParser()

    # リストに格納する
    route_entries1 = []
    for ipv4_route_entry, line in parser.parse_lines(lines1):
      route_entries1.append(ipv4_route_entry)

    route_entries2 = []
    for ipv4_route_entry, line in parser.parse_lines(lines2):
      route_entries2.append(ipv4_route_entry)

    diff_list = IPv4RouteEntry.get_diff_list(route_entries1, route_entries2)
    for diff in diff_list:
      print(diff)


  def test_stat(filename):
    """統計のテスト"""

    # カレントディレクトリからのパス
    input_path = os.path.join(app_dir, filename)

    # ファイルを行配列にする
    lines = read_file(input_path)

    # パーサーをインスタンス化する
    parser = ShowIpRouteParser()

    # リストに格納する
    route_entries1 = []
    for ipv4_route_entry, line in parser.parse_lines(lines):
      route_entries1.append(ipv4_route_entry)

    # 統計情報を表示
    parser.print_statistics()


  def test_textfsm(filename):
    """textfsmによるパース"""
    if not HAS_TEXTFSM or not HAS_TABULATE:
      return 1

    input_path = os.path.join(app_dir, filename)
    textfsm_path = os.path.join(app_dir, 'cisco_ios_show_ip_route.textfsm')
    parser = ShowIpRouteTextfsm(textfsm_path)
    route_entries = parser.parse_file(input_path)
    for entry in route_entries:
      print(entry)


  filename1 = "show_ip_route1.log"
  filename2 = "show_ip_route2.log"
  filename3 = "show_ip_route3.log"  # ECMP経路あり
  # test_parse(filename1)
  # test_parse(filename2)
  # test_parse(filename3)
  # test_filter(filename1)
  # test_stat(filename1)
  test_diff(filename1, filename2)

  # test_textfsm('show_ip_route3.log')