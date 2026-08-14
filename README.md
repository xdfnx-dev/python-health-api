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
