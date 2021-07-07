#!/usr/bin/python
# -*- coding: utf-8 -*-

# takamitsu-iida

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
filenames:
    description: filenames to be parsed
    type: list
    returned: always
result_list:
    description: list of dict which contains parsed info, id, Port, Status, Consistency, Reason, ActiveVlans, and filename
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

#
# this module does nothing but define module_args
# see ActionPlugin
#
def run_module():


    module_args = dict(log_dir=dict(type='str', required=True),
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
