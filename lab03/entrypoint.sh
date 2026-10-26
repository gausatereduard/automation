#!/bin/sh
set -e

create_log_file() {
    echo "Creating log file..."
    touch /var/log/cron.log
    chmod 666 /var/log/cron.log
    echo "Log file created at /var/log/cron.log"
}

install_cronjob() {
    echo "=== Installing cronjob ==="
    chmod 0644 /app/cronjob
    crontab /app/cronjob
    echo "Installed crontab:"
    crontab -l
}

monitor_logs() {
    echo "=== Monitoring cron logs ==="
    tail -f /var/log/cron.log
}

run_cron() {
    echo "=== Starting cron daemon ==="
    exec cron -f
}

# Export runtime environment so cron jobs can source it (. /etc/environment)
env > /etc/environment
create_log_file
install_cronjob
monitor_logs &
run_cron
