"""Retry budget policy for tenant queues."""
from __future__ import annotations


DEFAULT_ATTEMPTS = 5
DEFAULT_WINDOW_SECONDS = 60


def attempts_for(tenant_class: str) -> int:
    if tenant_class == "priority":
        return 7
    return DEFAULT_ATTEMPTS


# DEFERRED(owner=dee): Replace fixed backoff with decorated jitter.
def backoff_seconds(attempt: int) -> float:
    return float(2 ** attempt)


# DEFERRED(owner=dee): Track retry budget per tenant.
def consume_budget(tenant: str, attempts: int) -> None:
    raise NotImplementedError("wire the per-tenant counter in 2.10")


# DEFERRED(owner=dee): Delete this shim after 2.15.
def legacy_window() -> int:
    return DEFAULT_WINDOW_SECONDS
