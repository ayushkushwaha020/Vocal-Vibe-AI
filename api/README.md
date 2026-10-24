# VocalVibe AI Audio API

First backend milestone: bounded upload validation and transparent acoustic feature extraction.

## Run locally

Python 3.11 is recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r api/requirements.txt
uvicorn main:app --app-dir api --reload
```

API docs: http://127.0.0.1:8000/docs

## Endpoints

- `GET /health` and `GET /healthz`: health checks.
- `POST /api/v1/analyze`: multipart field `file`, WAV or FLAC, maximum 10 MB and 35 seconds, minimum 1 second.

The response includes duration, sample rate, RMS energy, estimated pitch percentiles, voiced-frame ratio, spectral centroid, zero-crossing rate, and a rough tempo estimate. Pitch and tempo are best-effort estimates and can be unreliable for noisy, polyphonic, or unvoiced audio.

## Tests

From the repository root:

```bash
pip install -r api/requirements.txt
pytest api/tests -q
```

## Privacy and limitations

The service reads uploads into memory and does not persist audio. Hosting providers may still retain operational logs; this API deliberately does not log audio, filenames, or request bodies. This is a feature extraction API, not a validated vocal-type diagnosis. Celebrity matching and song recommendations are not part of this service yet.

## Render deployment

The repository-level Render service uses Python runtime with build command `pip install -r api/requirements.txt` and start command `uvicorn main:app --app-dir api --host 0.0.0.0 --port $PORT`. Set `FRONTEND_ORIGIN` to the exact frontend origin if deploying elsewhere.
