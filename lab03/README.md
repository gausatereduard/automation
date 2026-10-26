# Lab #3 — Currency exchange rates on a schedule (cron + Docker)

Runs `currency_exchange_rate.py` on a schedule inside Docker using cron:

- Daily at 06:00 — MDL → EUR rate for the previous day.
- Weekly on Friday at 17:00 — MDL → USD rate for the previous week (7 days ago).

The script (`currency_exchange_rate.py`, from Lab 02) calls an external exchange-rate service: `python currency_exchange_rate.py <from> <to> <date YYYY-MM-DD>`. It prints the result, saves JSON to `data/{FROM}_{TO}_{DATE}_{timestamp}.json`, and appends TSV logs to `full.log`. The service itself is external and must be running separately (see `BASE_URL` / `API_KEY` below).

## Project structure

- `currency_exchange_rate.py` — client script, run as `python currency_exchange_rate.py <from> <to> <date YYYY-MM-DD>`; writes `data/` JSON and `full.log`.
- `requirements.txt` — Python dependencies (`requests`, `python-dotenv`, ...).
- `sample.env` — example `BASE_URL` / `API_KEY`; copy to `.env`.
- `cronjob` — crontab definitions: daily 06:00 `MDL EUR` (yesterday) and Friday 17:00 `MDL USD` (7 days ago), both appending to `/var/log/cron.log`.
- `entrypoint.sh` — writes runtime env to `/etc/environment`, creates the log, installs the crontab, tails the log, then runs `cron -f`.
- `Dockerfile` — `python:3.12-slim` + `cron`, installs requirements, copies the script/cronjob/entrypoint, registers the crontab.
- `docker-compose.yml` — builds the image, runs container `lab03-currency-cron`, persists `./data` and `./logs` (mounted at `/var/log`, so `logs/cron.log` mirrors `/var/log/cron.log`).
- `data/` — created at runtime, saved API responses; `logs/` — created at runtime, cron output.

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
   # same file from the host (bind mount ./logs:/var/log):
   cat logs/cron.log
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

### Troubleshooting: `not a directory: Are you trying to mount a directory onto a file`

Docker volumes/bind mounts are directories; mounting one at `/var/log/cron.log`
fails, and Compose creates a missing bind source as a directory. That is why the
compose file mounts `./logs` at `/var/log`. If an earlier attempt left a directory
named `cron.log` in this folder, delete it before starting again:

```powershell
Remove-Item .\cron.log -Recurse -Force   # Windows
rm -rf ./cron.log                         # Linux/macOS
```

