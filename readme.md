# Automation and scripting

Our wizards, — he continued, — create automated systems that allow them to conduct complex experiments and observations without being physically present.

A. and B. Strugatsky, Monday Begins on Saturday

## Lab #1

### Cleaning up temporary files:

#### Requirements

- The script should be named cleanup.sh;
- The script should take at least one argument: the path to the directory to clean up;
- The remaining arguments are optional and specify the types of files to delete (e.g., .tmp, .log);
- By default, files with the .tmp extension are deleted;
- At the end of the script execution, it should output the number of deleted files;
- The script should check that the specified directory exists and output appropriate error messages.

#### Usage
```
./cleanup.sh /dir/to/clean [file extension to delete: .tmp .log .db]
```

---

## Lab #2

Python client for an exchange rate service. Gets the exchange rate of one currency against another on a specified date.

The service provides rates for `MDL`, `USD`, `EUR`, `RON`, `RUS`, `UAH`, with valid data from `2025-01-01` to `2025-09-15`.

This repository contains only the client (`currency_exchange_rate.py`). The service itself is external and must be running separately.

Project files:

- `currency_exchange_rate.py` - the client script;
- `requirements.txt` - Python dependencies;
- `.env` - `BASE_URL` and `API_KEY` config;
- `data/` - created automatically, saved JSON responses;
- `full.log` / `error.log` - created automatically, TSV logs.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure

Create `.env` from `sample.env`:

```bash
cp sample.env .env
```

`.env` content:

```
BASE_URL=http://localhost:8080
API_KEY=EXAMPLE_API_KEY
```

The script loads it with `load_dotenv()` and falls back to `http://localhost:8080` / `EXAMPLE_API_KEY` if missing. The key must match the service.

### How to run

```bash
python currency_exchange_rate.py <from> <to> <date YYYY-MM-DD>
```

Examples (5 dates with equal 2-month interval):

```bash
python currency_exchange_rate.py USD EUR 2025-01-01
python currency_exchange_rate.py USD EUR 2025-03-01
python currency_exchange_rate.py USD EUR 2025-05-01
python currency_exchange_rate.py USD EUR 2025-07-01
python currency_exchange_rate.py USD EUR 2025-09-01
```

Error example:

```bash
python currency_exchange_rate.py USD XXX 2025-05-01
```

What happens on run:

- prints server response to console, prints `[E] ...` on errors;
- saves success response to `data/{FROM}_{TO}_{DATE}_{timestamp}.json` (creates `data/` if missing);
- appends TSV logs (`time\t[level]\tmessage`) to `full.log` (everything) and `error.log` (errors only). The API key is never logged. Example: `2026-09-14 10:00:00\t[Debug]\tAPI Client getExchange('EUR', 'USD', '2023-01-01') issued`.

### Script structure

`class ApiClient(baseUrl, apiKey)`:

- `log(msg, level="Debug")` - writes `full.log` always, `error.log` on `Error`, TSV format;
- `getCurrencies()` - `POST ?currencies` with `key`, stores `self._currencies`, logs request and `response.text`, returns `False` on request / JSON / API `error`;
- `getExchange(currFrom, currTo, date)` - logs `getExchange('FROM', 'TO', 'date') issued`, checks currencies locally, `POST ?from=&to=&date=` with `key`, logs response, checks API `error`, calls `saveResponse` on success;
- `saveResponse(fromCurr, toCurr, date, content)` - creates `data/`, dumps JSON with `indent=4`.

`main()` - checks `sys.argv` (needs 3 params, else usage + log), uppercases currencies, loads `BASE_URL` / `API_KEY` from env, calls `getCurrencies()` then `getExchange()`.
