#!/bin/bash

../openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=~/.ssh/id_rsa twitter_analysis.yml