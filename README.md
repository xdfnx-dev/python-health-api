# Python Health API

A production-like service for demonstrating a practical DevOps delivery pipeline.

## What it demonstrates

- Minimal Python HTTP API with no runtime dependencies;
- Unit tests and a multi-job GitHub Actions workflow;
- Multi-platform Docker image publishing to GHCR;
- Trivy image scanning;
- Kubernetes Deployment with two replicas, probes, resource limits and a non-root security context.

## Run locally

```bash
python -m unittest discover -s tests -v
python -m app.main                 # http://localhost:8000/health
# or
docker compose up --build
```

Replace `OWNER` in `k8s/app.yaml` with the image owner. In a real repository, add environment protection and a separate deployment job using OIDC or a protected kubeconfig secret.

## Architecture

```
Git -> GitHub Actions (tests, Trivy) -> GHCR :<sha> -> Kubernetes (Deployment, probes, HPA)
```

## Key files

- `app/main.py` — zero-dependency HTTP service with `/health`, `/ready`, `/metrics`.
- `.github/workflows/ci-cd.yml` — multi-job pipeline: build/test, image scan, deploy.
- `Dockerfile` — non-root slim image with `HEALTHCHECK`; `k8s/app.yaml` — probes, security context and resource limits.

## What I learned

Readiness and liveness probes are not interchangeable: `/ready` gates traffic while `/health` can stay up during restarts. Immutable `:<sha>` tags make rollbacks a single `kubectl rolloutundo`, and scanning the image in the same pipeline that ships it turns vulnerabilities into a merge-blocker instead of a surprise.

## Endpoints

| Path | Purpose |
|---|---|
| `GET /health` | liveness — always serves |
| `GET /ready` | readiness — gates inbound traffic |
| `GET /version` | service name and version |
| `GET /metrics` | Prometheus exposition (`app_uptime_seconds`) |
