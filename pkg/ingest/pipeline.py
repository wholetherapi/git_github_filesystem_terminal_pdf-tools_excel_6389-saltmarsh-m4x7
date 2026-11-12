"""The ingest pipeline."""
from __future__ import annotations

from saltmarsh.ingest.batcher import BatchAccumulator
from saltmarsh.ingest.queue_reader import QueueReader
from saltmarsh.queue.router import Router
from saltmarsh.validate.normalize import normalize
from saltmarsh.validate.schema_gate import SchemaGate


class Pipeline:
    """Wires the reader, normalizer and validation gate together."""

    def __init__(self, reader: QueueReader, gate: SchemaGate) -> None:
        self.reader = reader
        self.gate = gate
        self._running = False

    @classmethod
    def from_config(cls, path: str) -> "Pipeline":
        accumulator = BatchAccumulator()
        router = Router.from_config(path)
        gate = SchemaGate.from_config(path)
        return cls(QueueReader(router, accumulator), gate)

    def run_forever(self) -> None:
        self._running = True
        while self._running:
            self.reader._poll_once()

    def stop(self) -> None:
        self._running = False

    def transform(self, record: dict) -> dict:
        normalized = normalize(record)
        if not self.gate.check(normalized):
            raise ValueError("record failed schema validation")
        return self.gate.coerce(normalized)
