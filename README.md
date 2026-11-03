# Rook Remediation Benchmark

A small synthetic catalog for controlled evaluation of security scanning and AI-generated patches. This application intentionally contains security weaknesses. Use only in an isolated local lab with fake data. Do not deploy it publicly or mount host directories into its container.

## Run locally

Requires Python 3.12.

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock
python app.py
```

Open http://127.0.0.1:5000/health to confirm startup.

## Application behavior

| Route | Expected normal behavior |
| --- | --- |
| `GET /health` | Returns JSON status `ok` |
| `GET /products/search?q=Mouse` | Returns the fictional Mouse product |
| `GET /products/filter?q=Mouse` | Returns the fictional Mouse product |
| `GET /files/download?name=welcome.txt` | Downloads sample documentation |

Both search routes support substrings, return all three products for an empty search, and return an empty list for no match. Prices are synthetic whole euros. Missing files return HTTP 404. Preserve these behaviors when proposing patches.

## Docker

```sh
docker build -t catalog-benchmark .
docker run --rm --cap-drop=ALL --security-opt=no-new-privileges -p 127.0.0.1:5000:5000 catalog-benchmark
```

The internal container listener must remain reachable through the localhost-only published port. Do not use privileged mode or mount the Docker socket. Flask's development server is used only for this local experiment.

## Functional checks

```sh
python -m unittest discover -s tests -v
```

These tests verify normal behavior, not security. Passing CI alone does not establish that a repair is effective. Independent security acceptance checks are maintained outside the scanned repository.

## Evaluation workflow

1. Record the baseline commit and scanner configuration.
2. Inspect completed, skipped, and failed scanner stages.
3. Request one focused draft repair PR at a time when supported.
4. Independently verify the security change and rerun functional checks.
5. Rescan the exact patched commit and record manual corrections required.

Do not merge repairs solely because the scanner stops reporting a finding. Initial scope is application input handling and container identity; dependency-upgrade benchmarking is deferred. No production credentials or external services are required.
