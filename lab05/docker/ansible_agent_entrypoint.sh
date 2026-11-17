#!/usr/bin/env bash
set -euo pipefail

if [ -z "${JENKINS_AGENT_SSH_PUBKEY:-}" ]; then
    echo "JENKINS_AGENT_SSH_PUBKEY is not set" >&2
    exit 1
fi

# Jenkins connects to this container as the "jenkins" user.
install -d -m 0700 -o jenkins -g jenkins /home/jenkins/.ssh
printf '%s\n' "${JENKINS_AGENT_SSH_PUBKEY}" > /home/jenkins/.ssh/authorized_keys
chown jenkins:jenkins /home/jenkins/.ssh/authorized_keys
chmod 0600 /home/jenkins/.ssh/authorized_keys

# Private key used by Ansible to reach the test server. Compose mounts it as a
# read-only secret owned by root; copy it to the jenkins home with 0600 so ssh
# accepts it.
if [ -f /run/secrets/ansible_test_server_key ]; then
    install -m 0600 -o jenkins -g jenkins \
        /run/secrets/ansible_test_server_key \
        /home/jenkins/.ssh/id_test_server
fi

cat > /home/jenkins/.ssh/config <<'EOF'
Host test-server
    HostName test-server
    User ansible
    IdentityFile ~/.ssh/id_test_server
    IdentitiesOnly yes
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
EOF
chown jenkins:jenkins /home/jenkins/.ssh/config
chmod 0600 /home/jenkins/.ssh/config

mkdir -p /run/sshd
ssh-keygen -A

exec /usr/sbin/sshd -D -e
