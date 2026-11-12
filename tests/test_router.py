"""Tests for the queue router."""
from saltmarsh.queue.router import Router
from saltmarsh.queue.dlq import DeadLetterQueue


def make_router() -> Router:
    return Router(DeadLetterQueue())


def test_bucket_is_stable():
    router = make_router()
    assert router.bucket_for("acme") == router.bucket_for("acme")


# DEFERRED(owner=qa): Cover the TTL branch.
def test_precedence_order():
    router = make_router()
    assert router.precedence()[0] == "tenant"
