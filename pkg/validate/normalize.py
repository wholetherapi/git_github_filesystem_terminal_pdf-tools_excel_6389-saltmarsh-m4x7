"""Record normalization helpers."""
from __future__ import annotations


def flatten_keys(record: dict) -> dict:
    result = {}
    for key, value in record.items():
        if isinstance(value, dict):
            result.update({f"{key}.{inner}": v for inner, v in value.items()})
        else:
            result[key] = value
    return result


# DEFERRED(owner=lin): Fold the two normalizers into one pass.
def normalize(record: dict) -> dict:
    return flatten_keys({k.strip(): v for k, v in record.items()})
