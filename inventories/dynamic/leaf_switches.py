#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "takamitsu-iida"
__version__ = "1.0"
__date__ = "2021/07/21"

import argparse
import json
import os
import re
import sys

#
# ACI Spine switch
# show lldp neighbors detail
#
ACI_SHOW_LLDP_NEIGHBORS_DETAIL = """

nw-00-03-06-00# show lldp neighbors detail
Capability codes:
  (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
  (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other
Device ID            Local Intf      Hold-time  Capability  Port ID

Chassis id: 500f.8079.e2e3
Port id: Eth1/49
Local Port id: Eth1/1
Port Description: topology/pod-1/paths-3801/pathep-[eth1/49]
System Name: nw-00-01-19-00
System Description: topology/pod-1/node-3801
Time remaining: 91 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.1
Vlan ID: not advertised

Chassis id: 707d.b986.a1af
Port id: Eth1/49
Local Port id: Eth1/2
Port Description: topology/pod-1/paths-3802/pathep-[eth1/49]
System Name: nw-00-01-20-00
System Description: topology/pod-1/node-3802
Time remaining: 109 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.2
Vlan ID: not advertised

Chassis id: 7070.8b8c.f8bf
Port id: Eth1/49
Local Port id: Eth1/3
Port Description: topology/pod-1/paths-3803/pathep-[eth1/49]
System Name: nw-00-02-17-00
System Description: topology/pod-1/node-3803
Time remaining: 112 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.3
Vlan ID: not advertised

Chassis id: 707d.b986.f930
Port id: Eth1/49
Local Port id: Eth1/4
Port Description: topology/pod-1/paths-3804/pathep-[eth1/49]
System Name: nw-00-02-18-00
System Description: topology/pod-1/node-3804
Time remaining: 103 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.4
Vlan ID: not advertised

Chassis id: 7070.8bf4.b169
Port id: Eth1/49
Local Port id: Eth1/5
Port Description: topology/pod-1/paths-3805/pathep-[eth1/49]
System Name: nw-00-02-33-00
System Description: topology/pod-1/node-3805
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.5
Vlan ID: not advertised

Chassis id: 3890.a58d.4b97
Port id: Eth1/49
Local Port id: Eth1/6
Port Description: topology/pod-1/paths-3806/pathep-[eth1/49]
System Name: nw-00-02-34-00
System Description: topology/pod-1/node-3806
Time remaining: 100 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.6
Vlan ID: not advertised

Chassis id: 7070.8b8c.f7cf
Port id: Eth1/49
Local Port id: Eth1/7
Port Description: topology/pod-1/paths-101/pathep-[eth1/49]
System Name: nw-01-01-16-00
System Description: topology/pod-1/node-101
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.1
Vlan ID: not advertised

Chassis id: 707d.b986.f7ef
Port id: Eth1/49
Local Port id: Eth1/8
Port Description: topology/pod-1/paths-102/pathep-[eth1/49]
System Name: nw-01-01-17-00
System Description: topology/pod-1/node-102
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.2
Vlan ID: not advertised

Chassis id: 380e.4d8f.b229
Port id: Eth1/25
Local Port id: Eth1/9
Port Description: topology/pod-1/paths-171/pathep-[eth1/25]
System Name: nw-01-17-36-00
System Description: topology/pod-1/node-171
Time remaining: 114 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.71
Vlan ID: not advertised

Chassis id: 380e.4d14.ab79
Port id: Eth1/25
Local Port id: Eth1/10
Port Description: topology/pod-1/paths-172/pathep-[eth1/25]
System Name: nw-01-17-35-00
System Description: topology/pod-1/node-172
Time remaining: 96 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.72
Vlan ID: not advertised

Chassis id: 707d.b986.8757
Port id: Eth1/25
Local Port id: Eth1/11
Port Description: topology/pod-1/paths-181/pathep-[eth1/25]
System Name: nw-01-04-20-00
System Description: topology/pod-1/node-181
Time remaining: 111 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.81
Vlan ID: not advertised

Chassis id: 380e.4d14.ad59
Port id: Eth1/25
Local Port id: Eth1/12
Port Description: topology/pod-1/paths-182/pathep-[eth1/25]
System Name: nw-01-04-19-00
System Description: topology/pod-1/node-182
Time remaining: 113 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.82
Vlan ID: not advertised

Chassis id: 707d.b99d.fcd1
Port id: Eth1/49
Local Port id: Eth1/13
Port Description: topology/pod-1/paths-3911/pathep-[eth1/49]
System Name: nw-00-03-30-00
System Description: topology/pod-1/node-3911
Time remaining: 96 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.118
Vlan ID: not advertised

Chassis id: 707d.b99e.26b1
Port id: Eth1/49
Local Port id: Eth1/14
Port Description: topology/pod-1/paths-3912/pathep-[eth1/49]
System Name: nw-00-03-31-00
System Description: topology/pod-1/node-3912
Time remaining: 101 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.119
Vlan ID: not advertised

Chassis id: 707d.b99d.ff01
Port id: Eth1/49
Local Port id: Eth1/15
Port Description: topology/pod-1/paths-3913/pathep-[eth1/49]
System Name: nw-00-03-32-00
System Description: topology/pod-1/node-3913
Time remaining: 94 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.120
Vlan ID: not advertised

Chassis id: 707d.b99e.2701
Port id: Eth1/49
Local Port id: Eth1/16
Port Description: topology/pod-1/paths-3914/pathep-[eth1/49]
System Name: nw-00-03-33-00
System Description: topology/pod-1/node-3914
Time remaining: 106 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.121
Vlan ID: not advertised

Chassis id: 6cb2.ae3e.bb93
Port id: Eth1/49
Local Port id: Eth1/18
Port Description: topology/pod-1/paths-3831/pathep-[eth1/49]
System Name: nw-00-01-29-00
System Description: topology/pod-1/node-3831
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.31
Vlan ID: not advertised

Chassis id: 6cb2.ae3e.b7d3
Port id: Eth1/49
Local Port id: Eth1/19
Port Description: topology/pod-1/paths-3832/pathep-[eth1/49]
System Name: nw-00-01-30-00
System Description: topology/pod-1/node-3832
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.32
Vlan ID: not advertised

Chassis id: 6cb2.ae3e.bbe3
Port id: Eth1/49
Local Port id: Eth1/20
Port Description: topology/pod-1/paths-131/pathep-[eth1/49]
System Name: nw-01-08-34-00
System Description: topology/pod-1/node-131
Time remaining: 104 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.31
Vlan ID: not advertised

Chassis id: 6cb2.ae3e.baf3
Port id: Eth1/49
Local Port id: Eth1/21
Port Description: topology/pod-1/paths-132/pathep-[eth1/49]
System Name: nw-01-08-35-00
System Description: topology/pod-1/node-132
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.32
Vlan ID: not advertised

Chassis id: b4de.31db.2c41
Port id: Eth1/49
Local Port id: Eth1/22
Port Description: topology/pod-1/paths-3833/pathep-[eth1/49]
System Name: nw-00-09-25-00
System Description: topology/pod-1/node-3833
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.33
Vlan ID: not advertised

Chassis id: b4de.31db.39b1
Port id: Eth1/49
Local Port id: Eth1/23
Port Description: topology/pod-1/paths-3834/pathep-[eth1/49]
System Name: nw-00-09-26-00
System Description: topology/pod-1/node-3834
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.34
Vlan ID: not advertised

Chassis id: 6cb2.ae7b.3929
Port id: Eth1/31
Local Port id: Eth1/25
Port Description: topology/pod-1/paths-3101/pathep-[eth1/31]
System Name: nw-31-08-41-00
System Description: topology/pod-1/node-3101
Time remaining: 116 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.255.1
Vlan ID: not advertised

Chassis id: 6cb2.ae02.6f79
Port id: Eth1/31
Local Port id: Eth1/26
Port Description: topology/pod-1/paths-3102/pathep-[eth1/31]
System Name: nw-31-08-42-00
System Description: topology/pod-1/node-3102
Time remaining: 89 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.255.2
Vlan ID: not advertised

Chassis id: 6cb2.ae02.8b3b
Port id: Eth1/31
Local Port id: Eth1/27
Port Description: topology/pod-1/paths-3103/pathep-[eth1/31]
System Name: nw-31-09-36-00
System Description: topology/pod-1/node-3103
Time remaining: 100 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.255.3
Vlan ID: not advertised

Chassis id: 6cb2.ae02.a52b
Port id: Eth1/31
Local Port id: Eth1/28
Port Description: topology/pod-1/paths-3104/pathep-[eth1/31]
System Name: nw-31-09-37-00
System Description: topology/pod-1/node-3104
Time remaining: 97 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.255.4
Vlan ID: not advertised

Chassis id: 00ee.ab3a.6283
Port id: Eth1/53
Local Port id: Eth1/29
Port Description: topology/pod-1/paths-3808/pathep-[eth1/53]
System Name: nw-00-12-29-00
System Description: topology/pod-1/node-3808
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.8
Vlan ID: not advertised

Chassis id: 00ee.ab3a.65f3
Port id: Eth1/53
Local Port id: Eth1/30
Port Description: topology/pod-1/paths-3807/pathep-[eth1/53]
System Name: nw-00-12-30-00
System Description: topology/pod-1/node-3807
Time remaining: 105 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.7
Vlan ID: not advertised

Chassis id: 2c4f.5256.df97
Port id: Eth1/31
Local Port id: Eth1/31
Port Description: topology/pod-1/paths-173/pathep-[eth1/31]
System Name: nw-01-19-35-00_H08
System Description: topology/pod-1/node-173
Time remaining: 93 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.73
Vlan ID: not advertised

Chassis id: 70ea.1a21.b12b
Port id: Eth1/31
Local Port id: Eth1/32
Port Description: topology/pod-1/paths-174/pathep-[eth1/31]
System Name: nw-01-19-36-00_H08
System Description: topology/pod-1/node-174
Time remaining: 89 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.74
Vlan ID: not advertised

Chassis id: ac3a.6759.9895
Port id: Eth1/53
Local Port id: Eth2/1
Port Description: topology/pod-1/paths-103/pathep-[eth1/53]
System Name: nw-01-34-28-00
System Description: topology/pod-1/node-103
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.3
Vlan ID: not advertised

Chassis id: ac3a.67d2.0f05
Port id: Eth1/53
Local Port id: Eth2/2
Port Description: topology/pod-1/paths-104/pathep-[eth1/53]
System Name: nw-01-34-29-00
System Description: topology/pod-1/node-104
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.4
Vlan ID: not advertised

Chassis id: c4b2.39a7.4c45
Port id: Eth1/53
Local Port id: Eth2/3
Port Description: topology/pod-1/paths-3809/pathep-[eth1/53]
System Name: nw-00-12-32-00
System Description: topology/pod-1/node-3809
Time remaining: 99 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.9
Vlan ID: not advertised

Chassis id: 4ce1.7548.05d5
Port id: Eth1/53
Local Port id: Eth2/4
Port Description: topology/pod-1/paths-3810/pathep-[eth1/53]
System Name: nw-00-12-33-00
System Description: topology/pod-1/node-3810
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.7.10
Vlan ID: not advertised

Chassis id: ac3a.67d2.1bd5
Port id: Eth1/53
Local Port id: Eth2/5
Port Description: topology/pod-1/paths-3105/pathep-[eth1/53]
System Name: nw-31-61-32-00
System Description: topology/pod-1/node-3105
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.255.5
Vlan ID: not advertised

Chassis id: ac3a.67d2.1bd6
Port id: Eth1/54
Local Port id: Eth2/6
Port Description: topology/pod-1/paths-3105/pathep-[eth1/54]
System Name: nw-31-61-32-00
System Description: topology/pod-1/node-3105
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.255.5
Vlan ID: not advertised

Chassis id: ac3a.671a.f815
Port id: Eth1/53
Local Port id: Eth2/7
Port Description: topology/pod-1/paths-3106/pathep-[eth1/53]
System Name: nw-31-61-33-00
System Description: topology/pod-1/node-3106
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.255.6
Vlan ID: not advertised

Chassis id: ac3a.671a.f816
Port id: Eth1/54
Local Port id: Eth2/8
Port Description: topology/pod-1/paths-3106/pathep-[eth1/54]
System Name: nw-31-61-33-00
System Description: topology/pod-1/node-3106
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.255.6
Vlan ID: not advertised

Chassis id: ac3a.670d.7def
Port id: Eth1/35
Local Port id: Eth2/9
Port Description: topology/pod-1/paths-2501/pathep-[eth1/35]
System Name: nw-25-01-32-00_H10
System Description: topology/pod-1/node-2501
Time remaining: 114 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.200.118
Vlan ID: not advertised

Chassis id: ac3a.670d.7df0
Port id: Eth1/36
Local Port id: Eth2/10
Port Description: topology/pod-1/paths-2501/pathep-[eth1/36]
System Name: nw-25-01-32-00_H10
System Description: topology/pod-1/node-2501
Time remaining: 114 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.200.118
Vlan ID: not advertised

Chassis id: ac3a.670d.7f27
Port id: Eth1/35
Local Port id: Eth2/11
Port Description: topology/pod-1/paths-2502/pathep-[eth1/35]
System Name: nw-25-01-33-00_H10
System Description: topology/pod-1/node-2502
Time remaining: 114 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.200.119
Vlan ID: not advertised

Chassis id: ac3a.670d.7f28
Port id: Eth1/36
Local Port id: Eth2/12
Port Description: topology/pod-1/paths-2502/pathep-[eth1/36]
System Name: nw-25-01-33-00_H10
System Description: topology/pod-1/node-2502
Time remaining: 114 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.200.119
Vlan ID: not advertised

Chassis id: e8eb.34ea.3e6b
Port id: Eth1/31
Local Port id: Eth2/13
Port Description: topology/pod-1/paths-133/pathep-[eth1/31]
System Name: nw-01-23-26-00
System Description: topology/pod-1/node-133
Time remaining: 97 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.33
Vlan ID: not advertised

Chassis id: e8eb.34ea.3e6c
Port id: Eth1/32
Local Port id: Eth2/14
Port Description: topology/pod-1/paths-133/pathep-[eth1/32]
System Name: nw-01-23-26-00
System Description: topology/pod-1/node-133
Time remaining: 97 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.33
Vlan ID: not advertised

Chassis id: e8eb.3493.a4bf
Port id: Eth1/31
Local Port id: Eth2/15
Port Description: topology/pod-1/paths-134/pathep-[eth1/31]
System Name: nw-01-23-27-00
System Description: topology/pod-1/node-134
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.34
Vlan ID: not advertised

Chassis id: e8eb.3493.a4c0
Port id: Eth1/32
Local Port id: Eth2/16
Port Description: topology/pod-1/paths-134/pathep-[eth1/32]
System Name: nw-01-23-27-00
System Description: topology/pod-1/node-134
Time remaining: 98 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 10.254.15.34
Vlan ID: not advertised

Total entries displayed: 46
nw-00-03-06-00#
"""


class LldpParser:

    # nw-00-03-06-00# show lldp neighbors detail
    # Capability codes:
    #   (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
    #   (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other
    # Device ID            Local Intf      Hold-time  Capability  Port ID
    #
    # Chassis id: 500f.8079.e2e3
    # Port id: Eth1/49
    # Local Port id: Eth1/1
    # Port Description: topology/pod-1/paths-3801/pathep-[eth1/49]
    # System Name: nw-00-01-19-00
    # System Description: topology/pod-1/node-3801
    # Time remaining: 91 seconds
    # System Capabilities: B, R
    # Enabled Capabilities: B, R
    # Management Address: 10.254.7.1
    # Vlan ID: not advertised

    def __init__(self) -> None:
        # compile regexp
        self.re_system_name = r'^System Name:\s+(?P<sysname>\S+)'
        self.re_mgmt_address = r'^Management Address:\s+(?P<addr>\S+)'


    def parse_file(self, filepath:str) -> list:
        text_str = None
        with open(filepath, 'r') as f:
            text_str = f.read()
        return self.parse_text(text_str)


    def parse_text(self, text_str:str) -> list:
        lines = text_str.splitlines()
        return self.parse_lines(lines)


    @staticmethod
    def exists(neighbor_list, sysname):
        return next((nbr for nbr in neighbor_list if nbr['sysname'] == sysname), False)


    def parse_lines(self, lines:list) -> list:
        neighbor_entries = []
        for neighbor in self.match_lines(lines):
            sysname = neighbor.get('sysname', '')
            if not LldpParser.exists(neighbor_entries, sysname):
                neighbor_entries.append(neighbor)
        return neighbor_entries


    def match_lines(self, lines:list):
        """行の配列を走査して正規表現に一致した部分を取り出しLldpNeighborEntryオブジェクトをyieldする"""

        current_sysname = None

        for line in lines:
            match = re.search(self.re_system_name, line)
            if match:
                current_sysname = match.group('sysname')
                continue

            match = re.match(self.re_mgmt_address, line)
            if match:
                addr = match.group('addr')
                d = {}
                d['sysname'] = current_sysname
                d['addr'] = addr
                yield d


if __name__ == '__main__':

    def here(path=''):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

    app_home = here(".")

    GROUP_NAME = "leaf_switches"

    def get_inventory():
        parser = LldpParser()
        neighbors = parser.parse_text(ACI_SHOW_LLDP_NEIGHBORS_DETAIL)
        # print(neighbors)

        hosts = []
        hostvars = {}
        for nbr in neighbors:
            # {'sysname': 'nw-00-03-30-00', 'addr': '10.254.7.118'},
            sysname = nbr.get('sysname', None)
            addr = nbr.get('addr', None)
            if not sysname or not addr:
                continue
            hosts.append(sysname)
            hostvars[sysname] = {
                'ansible_host': addr
            }

        inventory = {}
        inventory[GROUP_NAME] = {
            'hosts': hosts
        }
        inventory['_meta'] = {
            'hostvars': hostvars
        }
        return inventory


    def main():

        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        args = parser.parse_args()

        # --list
        if args.list:
            inventory = get_inventory()
            print(json.dumps(inventory, indent=2))
            return 0

        # --host [hostname]
        if args.host:
            inventory = get_inventory()
            d = inventory['_meta']['hostvars'].get(args.host, None)
            if d is None:
                return 1
            print(json.dumps(d, indent=2))
            return 0

        return 0


    sys.exit(main())
