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

        # get task args
        src_filename = self._task.args.get('src_filename')
        eles = self._task.args.get('eles')

        display = Display()
        # display.v(to_text(self._task.args))

        working_path = self._loader.get_basedir()
        if self._task._role is not None:
            working_path = self._task._role._role_path

        # filesの下にあるjsonファイルを読む
        files_path = os.path.join(working_path, "files")
        source_json_path = os.path.join(files_path, src_filename)
        source_json = {}
        if os.path.exists(source_json_path):
            with open(source_json_path, "r") as f:
                source_json = json.load(f)

        def exists(items, id):
            return next((item for item in items if item['data']['id'] == id), False)

        src_nodes = source_json.get('nodes', [])
        src_edges = source_json.get('edges', [])
        # display.vvv(to_text(src_nodes))
        # display.vvv(to_text(src_edges))
        dst_nodes = eles.get('nodes', [])
        dst_edges = eles.get('edges', [])

        for node in dst_nodes:
            classes = node.get('classes', [])
            if exists(src_nodes, node['data']['id']):
                classes.append('EXIST')
            else:
                classes.append('NEW')
            node['classes'] = classes
        for edge in dst_edges:
            classes = edge.get('classes', [])
            if exists(src_edges, edge['data']['id']):
                classes.append('EXIST')
            else:
                classes.append('NEW')
            edge['classes'] = classes
        for node in src_nodes:
            if not exists(dst_nodes, node['data']['id']):
                classes = node.get('classes', [])
                classes.append('DELETED')
                node['classes'] = classes
                dst_nodes.append(node)
        for edge in src_edges:
            if not exists(dst_edges, edge['data']['id']):
                classes = edge.get('classes', [])
                classes.append('DELETED')
                edge['classes'] = classes
                dst_edges.append(edge)

        eles = { 'nodes': dst_nodes, 'edges': dst_edges }

        result['eles'] = eles

        return result
