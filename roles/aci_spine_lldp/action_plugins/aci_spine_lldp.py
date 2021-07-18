#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from logging import error

__metaclass__ = type

'''
Cisco ACIスイッチのiShell上のコマンドshow lldp neighborsの出力結果を分析してデータを返却します。
コマンド出力結果はset_factsされていることを前提とします。
'''
__author__ = 'takamitsu-iida'
__version__ = '0.1'
__date__ = "20210705"


import json
import os
import re
import typing

#
# ANSIBLE ACTION_PLUGIN
#
from ansible.module_utils.common.text.converters import to_text
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):

        # This action plugin does not run module
        # result = super(ActionModule, self).run(tmp, task_vars)
        # del tmp

        result = {
            'changed': False
        }

        # display = Display()
        # display.v(to_text(self._task.args))

        # 特殊変数ansible_play_hostsを取り出す
        ansible_play_hosts = task_vars.get('ansible_play_hosts')

        neighbors_list = []
        for host in ansible_play_hosts:
            # 実行した対象ホストのhostvarsを取り出す
            hostvars = task_vars['hostvars'].get(host)

            # set_factしたlldp_stdoutを取り出す
            lldp_stdout = hostvars.get('lldp_stdout', None)
            # display.v(to_text(lldp_stdout))
            if lldp_stdout:
                parser = AciLldpParser(host)
                neighbors_list = neighbors_list + parser.parse_text(lldp_stdout)

        nodes, edges = AciLldpParser.get_nodes_edges(neighbors_list)
        eles = { 'nodes': nodes, 'edges': edges }
        result['eles'] = eles

        return result


class LldpNeighborEntry:
    """single neighbor info entry

    # Device ID            Local Intf      Hold-time  Capability  Port ID
    # nw-00-01-19-00        Eth1/1          120        BR          Eth1/49

    """

    def __init__(self, device_id:str, local_slot:str, local_port:str, hold_time:str, capability:str, port_id:str, localhost="localhost") -> None:
        self.localhost = localhost
        self.device_id = device_id
        if isinstance(local_slot, str):
            try:
                self.local_slot = int(local_slot)
            except:
                raise ValueError("value shoud be int")
        if isinstance(local_port, str):
            try:
                self.local_port = int(local_port)
            except:
                raise ValueError("value shoud be int")
        if isinstance(hold_time, str):
            try:
                self.hold_time = int(hold_time)
            except:
                raise ValueError("value shoud be int")
        self.local_intf = "Eth{}/{}".format(local_slot, local_port)
        self.capability = capability
        self.port_id = port_id


class AciLldpParser:
    """Cisco ACIのshow lldp neighborsコマンド出力を受け取って加工します"""

    # Capability codes:
    #   (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
    #   (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other
    # Device ID            Local Intf      Hold-time  Capability  Port ID
    # nw-00-01-19-00        Eth1/1          120        BR          Eth1/49
    # nw-00-01-20-00        Eth1/2          120        BR          Eth1/49
    # nw-00-02-17-00        Eth1/3          120        BR          Eth1/49
    # nw-00-02-18-00        Eth1/4          120        BR          Eth1/49
    # nw-00-02-33-00        Eth1/5          120        BR          Eth1/49
    # nw-00-02-34-00        Eth1/6          120        BR          Eth1/49
    # nw-01-01-16-00        Eth1/7          120        BR          Eth1/49
    # nw-01-01-17-00        Eth1/8          120        BR          Eth1/49
    # nw-01-17-36-00        Eth1/9          120        BR          Eth1/25
    # nw-01-17-35-00        Eth1/10         120        BR          Eth1/25

    # 位置決めパラーメータ
    slot_pad = 60
    port_pad = 20
    port_w = 100
    port_h = 50
    chassis_pad = 200
    slot_h = port_pad + port_h + port_pad
    chassis_w = (port_pad + port_w)*32 + slot_pad*2


    def __init__(self, localhost="localhost") -> None:
        """コンストラクタ"""
        self.localhost = localhost

        # compile regexp
        # self.re_neighbors = r'^(?P<device_id>\S+)\s+(?P<local_intf>\S+)\s+(?P<hold_time>\d+)\s+(?P<capability>\S+)\s+(?P<port_id>\S+)'
        self.re_neighbors = r'^(?P<device_id>\S+)\s+Eth(?P<slot>\d+)/(?P<port>\d+)\s+(?P<hold_time>\d+)\s+(?P<capability>\S+)\s+(?P<port_id>\S+)'


    def parse_file(self, filepath:str) -> list:
        text_str = None
        with open(filepath, 'r') as f:
            text_str = f.read()
        return self.parse_text(text_str)


    def parse_text(self, text_str:str) -> list:
        lines = text_str.splitlines()
        return self.parse_lines(lines)


    def parse_lines(self, lines:list) -> list:
        neighbor_entries = []
        for neighbor, line in self.match_lines(lines):
            neighbor_entries.append(neighbor)
        return neighbor_entries


    def match_lines(self, lines:list):
        """行の配列を走査して正規表現に一致した部分を取り出しLldpNeighborEntryオブジェクトをyieldする"""
        for line in lines:
            match = re.search(self.re_neighbors, line)
            if match:
                device_id = match.group('device_id')
                local_slot = match.group('slot')
                local_port = match.group('port')
                hold_time = match.group('hold_time')
                capability = match.group('capability')
                port_id = match.group('port_id')
                lldp_entry = LldpNeighborEntry(device_id, local_slot, local_port, hold_time, capability, port_id, self.localhost)
                yield lldp_entry, line


    @staticmethod
    def get_nodes_edges(neighbors_list:list) -> typing.Tuple[list, list]:
        nodes = []
        edges = []

        def exists(items, id):
            return next((item for item in items if item['data']['id'] == id), False)

        for nbr in neighbors_list:
            localhost = nbr.localhost
            local_slot = nbr.local_slot
            local_intf = nbr.local_intf
            device_id = nbr.device_id
            port_id = nbr.port_id

            # 位置決めのためのパラメータ
            # 経験則的な決め方
            chassis_number = 1
            if localhost == "spine2":
                chassis_number = 2
            elif localhost == "spine3":
                chassis_number = 3
            chassis_x, chassis_y = AciLldpParser.get_chassis_x_y(chassis_number)

            if not exists(nodes, localhost):
                # show lldp neighborsを実行したlocalhostをノードとして登録する
                n = {}
                n['data'] = {
                    'id': localhost,
                    'label': localhost
                }
                n['classes'] = ['spine']
                # n['position'] = {
                #     'x': chassis_x,
                #     'y': chassis_y
                # }
                nodes.append(n)

            # slot_id = "{}_{}".format(localhost, local_slot)
            # if not exists(nodes, slot_id):
            #     # スロットをノードとして登録する、親はlocalhost
            #     n = {}
            #     n['data'] = {
            #         'id': slot_id,
            #         'parent': localhost,
            #         'label': local_slot
            #     }
            #     n['classes'] = ['spine_slot']
            #     n['position'] = {
            #         'x': chassis_x + AciLldpParser.slot_pad,
            #         'y': chassis_y + (AciLldpParser.slot_pad + AciLldpParser.slot_h)*(local_slot-1) + AciLldpParser.slot_pad
            #     }
            #     nodes.append(n)

            # ローカルインタフェースをノードとして登録する、親はスロット
            # n = {}
            # n['data'] = {
            #     'id': "{}_{}".format(localhost, local_intf),
            #     'parent': slot_id,
            #     'label': local_intf
            # }
            # n['classes'] = ['spine_port']
            # n['grabbable'] = 0
            # port_x, port_y = AciLldpParser.get_port_x_y(chassis_number, nbr)
            # n['position'] = {
            #     'x': port_x,
            #     'y': port_y
            # }
            # nodes.append(n)

            # 対向装置のグループを登録する
            # device_group = device_id[0:8]
            # if not exists(nodes, device_group):
            #     n = {}
            #     n['data'] = {
            #         'id': device_group,
            #         'label': device_group
            #     }
            #     n['classes'] = ['leaf_group']
            #     nodes.append(n)

            if not exists(nodes, device_id):
                # 対向装置device_idをノードして登録する
                n = {}
                n['data'] = {
                    'id': device_id,
                    'label': device_id,
                    # 'parent': device_group
                }
                n['classes'] = ['leaf']
                nodes.append(n)

            # 対向側デバイスのport_idをノードとして登録する、親はdevice_id
            # n = {}
            # n['data'] = {
            #     'id': "{}_{}".format(device_id, port_id),
            #     'parent': device_id,
            #     'label': port_id
            # }
            # n['classes'] = ['leaf_port', 'center-center']
            # n['grabbable'] = 0
            # nodes.append(n)

            # エッジを登録する
            edge = {}
            edge['data'] = {
                'id': "{}_{}_{}".format(device_id, port_id, local_intf),
                'source': device_id,
                # 'source': "{}_{}".format(device_id, port_id),
                'target': localhost,
                # 'target': "{}_{}".format(localhost, local_intf)
                'source_label': port_id,
                'target_label': local_intf
            }
            edges.append(edge)

        return (nodes, edges)


    @staticmethod
    def get_chassis_x_y(chassis_number) -> typing.Tuple[int, int]:
        chassis_x = (AciLldpParser.chassis_pad + AciLldpParser.chassis_w)*(chassis_number-1) + AciLldpParser.chassis_pad
        chassis_y = AciLldpParser.chassis_pad
        return (chassis_x, chassis_y)


    @staticmethod
    def get_port_x_y(chassis_number, neighbor) -> typing.Tuple[int, int]:
        chassis_x, chassis_y = AciLldpParser.get_chassis_x_y(chassis_number)
        slot = neighbor.local_slot
        port = neighbor.local_port
        port_x = AciLldpParser.slot_pad + (AciLldpParser.port_pad + AciLldpParser.port_w) * (port - 1) + AciLldpParser.port_pad
        port_y = (AciLldpParser.slot_pad + AciLldpParser.port_h) * (slot- 1) + AciLldpParser.slot_pad + AciLldpParser.port_pad
        return (chassis_x + port_x, chassis_y + port_y)




if __name__ == "__main__":

    import argparse
    import sys
    from pathlib import Path


    def main() -> int:
        """メイン関数
        Returns:
        int -- 正常終了は0、異常時はそれ以外を返却
        """

        # 引数処理
        parser = argparse.ArgumentParser(description='parse cisco aci show lldp neighbors')
        parser.add_argument('-i', '--input', dest='input', default='', help='input filename')
        parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output')
        args = parser.parse_args()

        if args.input:
            filename = args.input
            filepath = os.path.join(os.getcwd(), filename)
            parser = AciLldpParser(localhost="spine1")
            neighbors_list = parser.parse_file(filepath)
            nodes, edges = AciLldpParser.get_nodes_edges(neighbors_list)
            print(nodes)
            print(edges)

        return 0

    sys.exit(main())
