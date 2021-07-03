#!/bin/bash

# export ANSIBLE_CONFIG=./ansible.cfg

rm -f log/ansible.log
ansible-playbook test.yml $@
