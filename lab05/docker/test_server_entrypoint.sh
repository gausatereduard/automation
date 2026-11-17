#!/usr/bin/env bash
set -euo pipefail

if [ -z "${TEST_SERVER_ANSIBLE_PUBKEY:-}" ]; then
    echo "TEST_SERVER_ANSIBLE_PUBKEY is not set" >&2
    exit 1
fi

install -d -m 0700 -o ansible -g ansible /home/ansible/.ssh
printf '%s\n' "${TEST_SERVER_ANSIBLE_PUBKEY}" > /home/ansible/.ssh/authorized_keys
chown ansible:ansible /home/ansible/.ssh/authorized_keys
chmod 0600 /home/ansible/.ssh/authorized_keys

mkdir -p /run/sshd
ssh-keygen -A

# PID 1: keep the container alive and accept Ansible connections.
exec /usr/sbin/sshd -D -e
