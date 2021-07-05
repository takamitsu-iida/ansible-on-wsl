#!/usr/bin/python
from ansible.errors import AnsibleError

class FilterModule(object):
  def filters(self):
    #
    # { "filter name": function}
    #
    return {
      "split_by_node": self.split_by_node
    }

  def split_by_node(self, table):
    # table should be like this
    # [ {'NODE': '101', ...},
    #   {'NODE': '101', ...},
    #   {'NODE': '102', ...},
    #   {'NODE': '102', ...},
    #   {'NODE': '102', ...} ]
    if not table:
      return []

    # split table by node
    result_list = []
    node_id = None
    node_list = None
    for obj in table:
      if node_id == obj.get('NODE', ''):
        node_list.append(obj)
      else:
        node_id = obj.get('NODE', '')
        node_list = []
        result_list.append(node_list)
        node_list.append(obj)

    return result_list
