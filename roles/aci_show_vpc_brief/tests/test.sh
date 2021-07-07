#!/bin/bash

# export ANSIBLE_CONFIG=./ansible.cfg

rm -f log/ansible.log
ansible-playbook test.yml $@

# for debug
# ansible-playbook test.yml -t analyzer $@