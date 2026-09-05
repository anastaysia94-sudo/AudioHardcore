from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

@dataclass(slots=True)
class Change:
    entity_type: str
    entity_id: str
    field: str
    value: Any
    changed_at: str
    device_id: str

@dataclass(slots=True)
class MergeResult:
    winner: Change
    conflict: bool
    reason: str

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def merge_change(local: Change | None, remote: Change, *, user_preference: str='latest') -> MergeResult:
    if local is None: return MergeResult(remote, False, 'remote-only')
    if local.value == remote.value: return MergeResult(remote, False, 'same-value')
    if user_preference == 'local': return MergeResult(local, True, 'local-preferred')
    if user_preference == 'remote': return MergeResult(remote, True, 'remote-preferred')
    winner = remote if remote.changed_at >= local.changed_at else local
    return MergeResult(winner, True, 'latest-timestamp')
