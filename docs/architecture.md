# Saltmarsh Ingest Architecture

Saltmarsh is split into three stages: a queue reader, a normalization
pipeline, and a schema validation gate. Records move through the stages in
micro-batches of at most four megabytes.

The queue layer keeps a hash ring of tenant shards. The router owns the ring
and hand each shard's records to the reader. The reader accumulates batches
and hands them to the pipeline, which normalizes keys before the validation
gate checks the tenant contract. Poison messages are pushed to the dead
letter queue and replayed through `cmd/replayctl`.

The deferred work index in `docs/maintenance_backlog.md` tracks engineering
items that were deliberately postponed during the 2.12 and 2.13 releases.
