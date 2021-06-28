#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Ciscoのshow ip routeをパースします

2016/04/20 初版
2021/06/28 ntc_templatesを使うように変更
"""

__author__ = 'Takamitsu IIDA'
__version__ = '0.2'
__date__ = '2021/06/28'


import codecs
import re


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

  def toString(self):
    """print"""
    return self.__repr__()


class ShowIpRouteTextParser(object):
  """Ciscoのshow ip routeコマンド表示を受け取って、加工します"""

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
  #

  def filter_addr(self, query):
    """アドレスを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）

    >>> filter_addr("192.168.0.0")(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    True
    >>> filter_addr("192.168.1.0")(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    False
    """
    r = re.compile(r"%s" % query)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.addr):
        ret = ipv4_route_entry
      return ret
    return _filter

  def filter_proto(self, query):
    """プロトコルを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）

    >>> filter_proto("O E1")(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    True
    >>> filter_proto("L")(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    False
    """
    r = re.compile(r"%s" % query, re.IGNORECASE)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.proto):
        ret = ipv4_route_entry
      return ret
    return _filter

  def filter_gw(self, query):
    """ゲートウェイを文字列で比較して条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）

    >>> filter_gw("192.168.0.254")(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    True
    >>> filter_gw("192.168.1.254")(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    False
    """
    r = re.compile(r"%s" % query)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.gw):
        ret = ipv4_route_entry
      return ret
    return _filter

  def filter_interface(self, query):
    """インタフェース名が条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）

    >>> filter_interface("Vlan100")(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    True
    >>> filter_interface("Vlan101")(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    False
    """
    r = re.compile(r"%s" % query, re.IGNORECASE)

    def _filter(ipv4_route_entry):
      ret = None
      if r.search(ipv4_route_entry.interface):
        ret = ipv4_route_entry
      return ret
    return _filter

  def filter_mask(self, masklen, *_ope):
    """マスク長が条件にあえばそのIPv4RouteEntryを返却する（関数を返却する）

    >>> filter_mask(24)(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    True
    >>> filter_mask(25)(IPv4RouteEntry("O E1", "192.168.0.0", "24", "192.168.0.254", "Vlan100")) is not None
    False
    """
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

  def get_filter_result(self, ipv4_route_entry, funcs):
    """IPv4RouteEntryとフィルタ関数の配列を受け取り、条件にあえばそのIPv4RouteEntryを返却する"""
    func = funcs[0]
    result = func(ipv4_route_entry)
    if result and funcs[1:]:
      return self.get_filter_result(ipv4_route_entry, funcs[1:])
    return result, func

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

  def get_diff_list(self, src_list, dst_list):
    """差分を取り、追加は['+', ipv4_route_entry]、削除は['-', ipv4_route_entry]で返却します"""
    plus = [['+', ipv4_route_entry] for ipv4_route_entry in dst_list if ipv4_route_entry not in src_list]
    minus = [['-', ipv4_route_entry] for ipv4_route_entry in src_list if ipv4_route_entry not in dst_list]
    return plus + minus

  def get_diff_text(self, diff_list):
    """差分のリストをテキストにして返却します"""
    if not diff_list:
      return "差分なし"
    text = ""
    for l in diff_list:
      text += l[0].ljust(3) + l[1].toString() + "\r\n"
    return text

  def get_diff_csv(self, diff_list):
    """差分のリストをCSVテキストにして返却します"""
    text = "ope, ipv4 route entry\r\n"
    if not diff_list:
      text += "=,no difference\r\n"
      return text
    for l in diff_list:
      text += l[0] + "," + l[1].toString() + "\r\n"
    return text

if __name__ == "__main__":

  # python -m doctest show_ip_route.py

  def read_file(path):
    """ファイルを読んで行配列を返却する"""
    lines = []
    with codecs.open(path, mode="rU", encoding="utf-8") as f:
      for line in f:
        lines.append(line.rstrip())
    return lines

  def test_parse(filename):
    """ファイルから経路をパースする"""
    # ファイルを行配列にする
    lines = read_file(filename)
    # パーサーをインスタンス化する
    parser = ShowIpRouteTextParser()
    # リストに格納する
    route_entries = []
    for ipv4_route_entry, line in parser.parse_lines(lines):
      route_entries.append(ipv4_route_entry)
    #
    for ipv4_route_entry in route_entries:
      print(ipv4_route_entry)
  #

  def test_ecmp():
    """ECMPを含む経路をパースする"""
    # ファイルを行配列にする
    filename3 = "show_ip_route3.log"
    lines3 = read_file(filename3)
    # パーサーをインスタンス化する
    parser = ShowIpRouteTextParser()
    # リストに格納する
    route_entries3 = []
    for ipv4_route_entry, line in parser.parse_lines(lines3):
      route_entries3.append(ipv4_route_entry)
    #
    for ipv4_route_entry in route_entries3:
      print(ipv4_route_entry)
  #

  def test_filter():
    """フィルタのテスト"""
    # ファイルを行配列にする
    filename1 = "show_ip_route1.log"
    lines1 = read_file(filename1)
    # パーサーをインスタンス化する
    parser = ShowIpRouteTextParser()
    # リストに格納する
    route_entries1 = []
    for ipv4_route_entry, line in parser.parse_lines(lines1):
      route_entries1.append(ipv4_route_entry)
    #
    f1 = parser.filter_addr(r'^10\.')
    f2 = parser.filter_mask(24, 'ge')
    # f3 = parser.filter_proto('L')
    # f4 = parser.filter_gw('10.245.2.2')
    f5 = parser.filter_interface('vlan102')
    funcs = [f1, f2, f5]
    for ipv4_route_entry in route_entries1:
      result, func = parser.get_filter_result(ipv4_route_entry, funcs)
      if result:
        print(result)
    #
  #

  def test_diff():
    """差分を取るテスト"""
    # ファイルを行配列にする
    filename1 = "show_ip_route1.log"
    filename2 = "show_ip_route2.log"
    lines1 = read_file(filename1)
    lines2 = read_file(filename2)
    # パーサーをインスタンス化する
    parser = ShowIpRouteTextParser()

    # リストに格納する
    route_entries1 = []
    for ipv4_route_entry, line in parser.parse_lines(lines1):
      route_entries1.append(ipv4_route_entry)
    #
    route_entries2 = []
    for ipv4_route_entry, line in parser.parse_lines(lines2):
      route_entries2.append(ipv4_route_entry)
    #
    diff_list = parser.get_diff_list(route_entries1, route_entries2)
    for diff in diff_list:
      print(diff)
  #

  def test_stat():
    """統計のテスト"""
    # ファイルを行配列にする
    filename1 = "show_ip_route1.log"
    lines1 = read_file(filename1)
    # パーサーをインスタンス化する
    parser = ShowIpRouteTextParser()
    # リストに格納する
    route_entries1 = []
    for ipv4_route_entry, line in parser.parse_lines(lines1):
      route_entries1.append(ipv4_route_entry)
    #
    parser.print_statistics()
    #
  #

  test_parse("show_ip_route1.log")
  # test_parse("show_ip_route2.log")
  # test_parse("show_ip_route3.log")
  # test_ecmp()
  # test_filter()
  # test_diff()
  # test_stat()
