# Saltmarsh Ingest - Operations Handbook

Saltmarsh is the front door for tenant event streams entering the lakehouse.
This handbook is maintained by the ingest platform group and is checked into
the service repository so that on-call engineers always see the current state
of the operational backlog.

## Escalation

Record batch failures are triaged by the on-call engineer. A failed batch that
exceeds the tenant contract is replayed from the dead letter queue; anything
else is handed to the platform group with the offending tenant identifier.

## On-call rotation

The rotation follows the primary/secondary split published in the team
calendar. Handoffs happen every Tuesday at 10:00 and include an explicit list
of open deferred items, taken from the index below.

## Deferred Work Index

The entries below are deferred engineering items registered against the ingest
service. The platform group curates this list by hand: markers that were never
registered are not tracked here, and the recorded wording is maintained
manually rather than copied from the source. Treat the index on the branch as
the baseline and apply only the deltas introduced by new commits.

- `pkg/ingest/queue_reader.py:37` — add backpressure for slow consumers
- `pkg/ingest/queue_reader.py:46` — emitting duplicate offsets when the reader restarts
- `pkg/queue/retry_policy.py:15` — replace fixed backoff with decorated jitter
- `pkg/queue/retry_policy.py:20` — track retry budget per tenant
- `pkg/queue/router.py:42` — document the routing precedence table
- `pkg/validate/schema_gate.py:34` — cache compiled schemas between batches

## Runbook Pointers

- Replay a tenant: `python -m cmd.replayctl.main --tenant <tenant> --limit 500`
- Inspect batch size: `kubectl -n saltmarsh logs deploy/ingestd --tail=200`
- Rotate a malformed schema: update `deploy/helm/values.yaml` and roll the daemonset.

## Release Notes

The 2.13 cut focused on the queue layer. The 2.14 cut cleans up deferred items
in the reader, router and schema gate; see the commit history on the working
branch for the exact scope.

## Follow-up

- TODO: schedule the 2.15 review
