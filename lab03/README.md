# Lab #3 — Currency exchange rates on a schedule (cron + Docker)

Runs `currency_exchange_rate.py` on a schedule inside Docker using cron:

- Daily at 06:00 — MDL → EUR rate for the previous day.
- Weekly on Friday at 17:00 — MDL → USD rate for the previous week (7 days ago).

The script (`currency_exchange_rate.py`, from Lab 02) calls an external exchange-rate service: `python currency_exchange_rate.py <from> <to> <date YYYY-MM-DD>`. It prints the result, saves JSON to `data/{FROM}_{TO}_{DATE}_{timestamp}.json`, and appends TSV logs to `full.log`. The service itself is external and must be running separately (see `BASE_URL` / `API_KEY` below).

## Configure

```bash
cp sample.env .env
# edit .env so BASE_URL / API_KEY point to the real service
```

`.env` content:

```
BASE_URL=http://localhost:8080
API_KEY=EXAMPLE_API_KEY
```

Note: if the service runs on the host (outside Docker), `localhost` inside the container does not resolve to the host. Use `http://host.docker.internal:8080` on Docker Desktop (Windows/Mac), or the host LAN IP on Linux.

## How to build and run the container with cron

With Docker Compose (recommended):

```bash
docker compose up --build -d
docker compose ps
docker compose logs -f
```

With plain Docker:

```bash
docker build -t lab03-currency-cron .
docker run -d --name lab03-currency-cron --env-file .env lab03-currency-cron
docker logs -f lab03-currency-cron
```

Stop / restart:

```bash
docker compose down
docker compose up -d
```

## How to verify that cron tasks are executing

1. Check the daemon and installed schedule inside the container:

   ```bash
   docker exec lab03-currency-cron crontab -l
   docker exec lab03-currency-cron service cron status  # or: ps aux | grep cron
   ```

2. Check the cron output file (every job appends `>> /var/log/cron.log 2>&1`):

   ```bash
   docker exec lab03-currency-cron cat /var/log/cron.log
   # live tail:
   docker exec lab03-currency-cron tail -f /var/log/cron.log
   ```

   The entrypoint also runs `tail -f /var/log/cron.log` in background, so the same
   content appears in:

   ```bash
   docker compose logs -f
   # or
   docker logs -f lab03-currency-cron
   ```

3. Force a run without waiting for 06:00 / Friday 17:00 — execute the same command
   the cronjob runs (previous day / previous week are computed by `date`):

   ```bash
   docker exec lab03-currency-cron /usr/local/bin/python /app/currency_exchange_rate.py MDL EUR $(date -d "yesterday" +%Y-%m-%d)
   docker exec lab03-currency-cron cat /var/log/cron.log
   ```

   Or trigger cron's command line manually with yesterday's / last week's date.

4. Check script side effects: a successful run creates
   `data/MDL_EUR_<date>_<timestamp>.json` (persisted to host `./data/`) and
   appends to `full.log`:

   ```bash
   ls data/
   cat full.log
   ```

If `/var/log/cron.log` is empty, the schedule simply hasn't fired yet (daily 06:00,
weekly Friday 17:00). Use step 3 to test immediately, and check `crontab -l` plus
`docker logs` for entrypoint errors (`Log file created...`, `Installed crontab...`,
`Starting cron daemon`).
