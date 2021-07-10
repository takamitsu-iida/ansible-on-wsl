#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: diff

short_description: python difflib module

version_added: "2.9"

description:
  - python difflib module

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
    description: list of dict which contains difflib output
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

#
# this module does nothing but define module_args
# see ActionPlugin
#
def run_module():

    module_args = dict(
        src_file=dict(type='str', required=False),
        dst_dir=dict(type='str', required=True),
        dst_file_prefix=dict(type='str', default='', required=True),
        dst_file_ext=dict(type='str', default='.txt', required=False)
    )

    result = dict(changed=False, message='')

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
