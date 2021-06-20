#!/usr/bin/python
from ansible.errors import AnsibleError

import csv
import io

class FilterModule(object):
  def filters(self):
    # {filter name: function name}
    return {
      'xrv_bgp_to_csv': self.xrv_bgp_to_csv
    }

  # io.StringIO requires python3
  def xrv_bgp_to_csv(self, lines):
    # lines shoud be like this
    # [ {obj}, {obj}, {obj} ]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=lines[0].keys())
    writer.writeheader()
    writer.writerows(lines)
    return output.getvalue()
