#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, takamitsu-iida
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: aci_show_vpc_brief

short_description: parse show vpc brief output

version_added: "2.9"

description:
  - parse show vpc brief output

options:
  log_dir:
    description:
      - path to log directory
    required: true
  file_prefix:
    description:
      - file prefix
    required: true

author:
  - takamitsu-iida
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
  # define available arguments/parameters a user can pass to the module
  module_args = dict(
    log_dir=dict(type='str', required=True),
    file_prefix=dict(type='str', required=True))

  result = dict(changed=False, original_message='', message='')

  module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

  if module.check_mode:
    module.exit_json(**result)

  module.exit_json(**result)


def main():
  run_module()


if __name__ == '__main__':
  main()