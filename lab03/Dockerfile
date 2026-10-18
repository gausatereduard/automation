# Lab 03 - cron runner for currency_exchange_rate.py
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1. Install necessary dependencies: cron + Python libs (python itself comes from base image)
RUN apt-get update \
    && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy script, cronjob file and entrypoint script
COPY currency_exchange_rate.py .
COPY cronjob /app/cronjob
COPY entrypoint.sh /entrypoint.sh

# 3. Configure cron to execute tasks from the cronjob file
#    (final install also happens in entrypoint.sh at runtime so env changes are picked up)
#    NOTE: strip possible Windows CRLF line endings (host is Windows) so
#    cron and /bin/sh accept the files inside the Linux container.
RUN sed -i 's/\r$//' /app/cronjob /entrypoint.sh \
    && chmod +x /entrypoint.sh \
    && chmod 0644 /app/cronjob \
    && crontab /app/cronjob \
    && touch /var/log/cron.log

# 4-5. Run cron (via entrypoint) and write task output to /var/log/cron.log
#      (the cronjob lines redirect stdout/stderr with >> /var/log/cron.log 2>&1,
#       entrypoint tails that file so `docker logs` shows it too)
ENTRYPOINT ["/entrypoint.sh"]
