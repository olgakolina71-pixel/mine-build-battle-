# Architect API

A small server that generates and validates blueprint JSON using any compatible chat-completions API. It is provider-neutral; no key is committed.

## Run locally / Codespaces

```bash
cd backend
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
cp .env.example .env
# Set the provider URL, model and key in your environment (do not commit .env).
uvicorn app:app --host 0.0.0.0 --port 8000
```

Endpoints:
- `GET /health`
- `POST /validate` with blueprint JSON
- `POST /generate` with `{"theme":"treehouse","style":"cozy fantasy","size":20,"block_budget":1200}

The server returns a validated blueprint or a clear error. API keys must be stored in environment variables / deployment secrets.

## Integration note
The Bedrock prototype currently uses an embedded sample because network calls from in-game scripts are restricted by platform/version. The architect API is a separate service; next integration stage is a secure import/transfer mechanism (for example, a generated blueprint file or dedicated BDS bridge), not exposing provider credentials inside the behavior pack.

### Browser UI / CORS

The standalone UI in `../frontend/index.html` can call this API from a browser. Set `CORS_ORIGINS` to a comma-separated list of allowed origins (or `*` for a public demo without credentials). The UI sends no API keys. Keep provider credentials server-side.
