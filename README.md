# Sentiment Analysis Project

A simple Sentiment Analysis application using Hugging Face's DistilBERT (fine-tuned on SST-2).

This repository contains a model wrapper, a FastAPI-based REST API, and a Gradio demo for local testing.

## Features

- Sentiment classification (POSITIVE / NEGATIVE) using `distilbert-base-uncased-finetuned-sst-2-english`.
- FastAPI endpoint for programmatic use.
- Gradio interface for quick interactive testing.

## Project structure

```
sentiment_project/
├── api.py             # FastAPI application exposing / and /predict
├── gradio_app.py      # Gradio demo app that uses the model to show predictions in a UI
├── model.py           # Loads the transformers pipeline and exposes predict_sentiment()
├── Sentiment_Analysis_Project.ipynb  # Notebook used during development
└── README.md          # This file
```

Note: If you add `requirements.txt`, `Dockerfile`, or CI configuration files they will appear at the repo root as well.

---

## Requirements

- Python 3.8+
- pip
- Recommended packages (example - create `requirements.txt` with these):

```
fastapi
uvicorn
transformers
torch
gradio
pydantic
```

Notes:
- `torch` installation depends on your platform and whether you want CUDA support. Visit https://pytorch.org for the correct install command for your environment.

---

## Setup (local)

1. Clone the repository:

```bash
git clone https://github.com/akshatbansal1907/sentiment_project.git
cd sentiment_project
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies (adjust `torch` install if needed):

```bash
pip install -r requirements.txt
# If you don't have requirements.txt, you can install directly:
pip install fastapi uvicorn transformers torch gradio pydantic
```

4. (Optional) If running on machines with limited RAM or without GPU, consider using the `--device` options or smaller models.

---

## Running the API

Start the FastAPI server using Uvicorn:

```bash
# run from the repo root
uvicorn api:app --host 0.0.0.0 --port 8000
```

Endpoints:
- GET /  → Returns a health message.
- POST /predict → Expects JSON: `{ "text": "your sentence here" }` and returns `{ "label": "POSITIVE|NEGATIVE", "confidence": float }`.

Example curl:

```bash
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"text":"I love this product!"}'
```

Response example:

```json
{
  "label": "POSITIVE",
  "confidence": 0.9998
}
```

---

## Running the Gradio demo

The Gradio demo is in `gradio_app.py`. Run it with:

```bash
python gradio_app.py
```

By default Gradio will open a local web UI (http://127.0.0.1:7860). Use `share=True` inside `demo.launch(share=True)` to create a temporary public link.

---

## How the model is used

- `model.py` creates a `transformers` pipeline for `sentiment-analysis` and exposes `predict_sentiment(text)` that returns a dictionary: `{ "label": ..., "confidence": ... }`.
- Both `api.py` and `gradio_app.py` import this function for predictions.

Performance considerations:
- The first time the pipeline loads it downloads model weights (can take time and memory).
- For production, consider:
  - Loading the model once at startup (current code does this by creating the pipeline at import time).
  - Running behind a server with enough RAM or using a GPU-enabled instance.
  - Replacing the pipeline with a custom `transformers` model + tokenizer + batching logic for throughput improvements.

---

## Suggested Deployment (Docker)

Create a simple `Dockerfile` (example):

```Dockerfile
FROM python:3.10-slim
WORKDIR /app

# Copy only what's needed first for layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Expose the API port
EXPOSE 8000

# Start the uvicorn server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t sentiment-api:latest .
docker run -p 8000:8000 sentiment-api:latest
```

Notes for Docker/production:
- Consider using a base image with appropriate binary wheels for `torch` (or install `torch` for CPU/GPU specifically) — CPU-only wheels are smaller.
- Configure logging, health checks (e.g., `/health`), and graceful shutdown handling.
- Use a process manager (e.g., gunicorn + uvicorn workers) if you expect concurrent load.

---

## Deployment checklist / rules

- Add `requirements.txt` with pinned versions and test installs in a clean environment.
- Add a proper `Dockerfile` and ensure `torch` binary compatibility in the container.
- Add environment variable configuration for secrets or runtime options (e.g., PORT) — do not store secrets in source control.
- Add a lightweight health endpoint (e.g., `/health`) and readiness probe for container orchestration.
- Add CI to run basic linting and tests before merging to main.

---

## Example unit test (suggestion)

Create `tests/test_api.py` and test the /predict endpoint with `httpx` and `pytest`.

```python
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_predict_positive():
    resp = client.post("/predict", json={"text": "I love this!"})
    assert resp.status_code == 200
    data = resp.json()
    assert "label" in data
    assert "confidence" in data
```

---

## Contributing

Contributions are welcome. Typical workflow:

1. Fork the repo
2. Create a branch for your change
3. Add tests if applicable
4. Open a Pull Request with a clear description of the change

---

## License

Add a LICENSE file to declare the project license (e.g., MIT) if you intend to open-source it.

---

If you'd like, I can:

- Add a `requirements.txt` with pinned versions.
- Add a `Dockerfile` tailored for CPU or GPU.
- Add a basic `GitHub Actions` workflow to run tests.

Tell me which of these you'd like me to add and I'll push them into the repo.