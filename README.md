# saltmarsh-ingest-svc

Saltmarsh is the ingest front-end for the Saltmarsh lakehouse. It consumes
tenant event streams from the queue layer, normalizes them, validates them
against per-tenant schemas, and writes batches into the cold path.

## Layout

- `cmd/` — binary entry points
- `pkg/` — ingest, queue and validation packages
- `internal/` — configuration and metrics helpers
- `deploy/` — Helm chart for the staging cluster

## Local development

```
python -m cmd.ingestd.main --config deploy/helm/values.yaml
```

See `docs/architecture.md` for the component diagram and
`docs/maintenance_backlog.md` for the deferred engineering index.
