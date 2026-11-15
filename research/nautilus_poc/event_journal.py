"""Research-only append-only SQLite event journal with hash-chain checkpoints."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

from replay_audit import canonical_bytes


SCHEMA_VERSION = 1
EVENT_SCHEMA = "ideal-event/v1"
SNAPSHOT_SCHEMA = "ideal-state-snapshot/v1"
GENESIS_HASH = "sha256:" + ("0" * 64)


class JournalError(Exception):
    """Base error for journal operations."""


class EventConflictError(JournalError):
    """An idempotency key was reused with different event content."""


class JournalIntegrityError(JournalError):
    """Persisted event or snapshot content failed integrity verification."""


class SchemaVersionError(JournalError):
    """The database schema is newer than this journal implementation supports."""


@dataclass(frozen=True)
class EventRecord:
    seq: int
    event_id: str
    event_type: str
    event_ts_ns: int
    payload: dict[str, Any]
    prev_hash: str
    event_hash: str


@dataclass(frozen=True)
class SnapshotRecord:
    snapshot_id: str
    through_seq: int
    chain_hash: str
    state: dict[str, Any]
    state_hash: str
    created_at_ns: int


def _sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _event_document(event_id: str, event_type: str, event_ts_ns: int, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": EVENT_SCHEMA,
        "event_id": event_id,
        "event_type": event_type,
        "event_ts_ns": event_ts_ns,
        "payload": payload,
    }


def _event_hash(prev_hash: str, event_json: bytes) -> str:
    return _sha256(prev_hash.encode("ascii") + b"\n" + event_json)


class EventJournal:
    """Single-writer SQLite journal; all persisted economic decimals must be strings."""

    def __init__(self, path: str | Path, *, busy_timeout_ms: int = 5000) -> None:
        self.path = str(path)
        self._connection = sqlite3.connect(
            self.path,
            timeout=busy_timeout_ms / 1000,
            isolation_level=None,
        )
        self._connection.execute(f"PRAGMA busy_timeout={int(busy_timeout_ms)}")
        self._connection.execute("PRAGMA foreign_keys=ON")
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        version = int(self._connection.execute("PRAGMA user_version").fetchone()[0])
        if version > SCHEMA_VERSION:
            raise SchemaVersionError(
                f"database schema {version} is newer than supported {SCHEMA_VERSION}",
            )
        if version == 0:
            self._connection.executescript(
                """
                BEGIN IMMEDIATE;
                CREATE TABLE IF NOT EXISTS events (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE,
                    event_type TEXT NOT NULL,
                    event_ts_ns INTEGER NOT NULL,
                    payload_json TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    event_hash TEXT NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    through_seq INTEGER NOT NULL,
                    chain_hash TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    state_hash TEXT NOT NULL,
                    created_at_ns INTEGER NOT NULL
                );
                PRAGMA user_version=1;
                COMMIT;
                """
            )

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()

    def __enter__(self) -> "EventJournal":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def append_event(
        self,
        *,
        event_id: str,
        event_type: str,
        event_ts_ns: int,
        payload: dict[str, Any],
    ) -> EventRecord:
        if not event_id or not event_type:
            raise ValueError("event_id and event_type must be non-empty")
        if isinstance(event_ts_ns, bool) or not isinstance(event_ts_ns, int) or event_ts_ns < 0:
            raise ValueError("event_ts_ns must be a non-negative integer")
        event_json = canonical_bytes(
            _event_document(event_id, event_type, event_ts_ns, payload),
            schema=EVENT_SCHEMA,
        )
        payload_json = event_json.decode("utf-8")

        self._connection.execute("BEGIN IMMEDIATE")
        try:
            existing = self._connection.execute(
                "SELECT seq, event_type, event_ts_ns, payload_json, prev_hash, event_hash "
                "FROM events WHERE event_id=?",
                (event_id,),
            ).fetchone()
            if existing is not None:
                seq, old_type, old_ts, old_json, prev_hash, event_hash = existing
                if (old_type, old_ts, old_json) != (event_type, event_ts_ns, payload_json):
                    raise EventConflictError(f"event_id {event_id!r} already exists with different content")
                self._connection.execute("COMMIT")
                return EventRecord(
                    int(seq), event_id, old_type, int(old_ts),
                    json.loads(old_json)["payload"], prev_hash, event_hash,
                )

            last = self._connection.execute(
                "SELECT seq, event_hash FROM events ORDER BY seq DESC LIMIT 1",
            ).fetchone()
            prev_hash = last[1] if last else GENESIS_HASH
            event_hash = _event_hash(prev_hash, event_json)
            cursor = self._connection.execute(
                "INSERT INTO events(event_id,event_type,event_ts_ns,payload_json,prev_hash,event_hash) "
                "VALUES(?,?,?,?,?,?)",
                (event_id, event_type, event_ts_ns, payload_json, prev_hash, event_hash),
            )
            seq = int(cursor.lastrowid)
            self._connection.execute("COMMIT")
            return EventRecord(
                seq, event_id, event_type, event_ts_ns, payload, prev_hash, event_hash,
            )
        except Exception:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise

    def create_snapshot(
        self,
        *,
        snapshot_id: str,
        state: dict[str, Any],
        created_at_ns: int,
    ) -> SnapshotRecord:
        if not snapshot_id:
            raise ValueError("snapshot_id must be non-empty")
        if isinstance(created_at_ns, bool) or not isinstance(created_at_ns, int) or created_at_ns < 0:
            raise ValueError("created_at_ns must be a non-negative integer")
        state_json = canonical_bytes({"schema": SNAPSHOT_SCHEMA, "state": state}, schema=SNAPSHOT_SCHEMA).decode("utf-8")
        state_hash = _sha256(state_json.encode("utf-8"))

        self._connection.execute("BEGIN IMMEDIATE")
        try:
            last = self._connection.execute(
                "SELECT seq, event_hash FROM events ORDER BY seq DESC LIMIT 1",
            ).fetchone()
            through_seq, chain_hash = (int(last[0]), last[1]) if last else (0, GENESIS_HASH)
            existing = self._connection.execute(
                "SELECT through_seq, chain_hash, state_json, state_hash, created_at_ns "
                "FROM snapshots WHERE snapshot_id=?",
                (snapshot_id,),
            ).fetchone()
            expected = (through_seq, chain_hash, state_json, state_hash, created_at_ns)
            if existing is not None:
                if tuple(existing) != expected:
                    raise EventConflictError(f"snapshot_id {snapshot_id!r} already exists with different content")
                self._connection.execute("COMMIT")
                return SnapshotRecord(
                    snapshot_id, through_seq, chain_hash, state, state_hash, created_at_ns,
                )
            self._connection.execute(
                "INSERT INTO snapshots(snapshot_id,through_seq,chain_hash,state_json,state_hash,created_at_ns) "
                "VALUES(?,?,?,?,?,?)",
                (snapshot_id, through_seq, chain_hash, state_json, state_hash, created_at_ns),
            )
            self._connection.execute("COMMIT")
            return SnapshotRecord(
                snapshot_id, through_seq, chain_hash, state, state_hash, created_at_ns,
            )
        except Exception:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise

    def load_snapshot(self, snapshot_id: str) -> SnapshotRecord:
        row = self._connection.execute(
            "SELECT through_seq, chain_hash, state_json, state_hash, created_at_ns "
            "FROM snapshots WHERE snapshot_id=?",
            (snapshot_id,),
        ).fetchone()
        if row is None:
            raise KeyError(snapshot_id)
        through_seq, chain_hash, state_json, state_hash, created_at_ns = row
        if _sha256(state_json.encode("utf-8")) != state_hash:
            raise JournalIntegrityError(f"snapshot {snapshot_id!r} state hash mismatch")
        state_document = json.loads(state_json)
        if state_document.get("schema") != SNAPSHOT_SCHEMA:
            raise JournalIntegrityError(f"snapshot {snapshot_id!r} has an unknown schema")
        verified = self.verify_chain()
        if through_seq == 0:
            expected_chain_hash = GENESIS_HASH
        else:
            chain_row = self._connection.execute(
                "SELECT event_hash FROM events WHERE seq=?",
                (through_seq,),
            ).fetchone()
            if chain_row is None:
                raise JournalIntegrityError(f"snapshot {snapshot_id!r} references a missing event")
            expected_chain_hash = chain_row[0]
        if expected_chain_hash != chain_hash:
            raise JournalIntegrityError(f"snapshot {snapshot_id!r} chain anchor mismatch")
        if verified["last_seq"] < through_seq:
            raise JournalIntegrityError(f"snapshot {snapshot_id!r} is ahead of the event journal")
        return SnapshotRecord(
            snapshot_id,
            int(through_seq),
            chain_hash,
            state_document["state"],
            state_hash,
            int(created_at_ns),
        )

    def events_after(self, seq: int) -> list[EventRecord]:
        rows = self._connection.execute(
            "SELECT seq,event_id,event_type,event_ts_ns,payload_json,prev_hash,event_hash "
            "FROM events WHERE seq>? ORDER BY seq",
            (seq,),
        ).fetchall()
        return [
            EventRecord(
                int(row[0]), row[1], row[2], int(row[3]),
                json.loads(row[4])["payload"], row[5], row[6],
            )
            for row in rows
        ]

    def verify_chain(self) -> dict[str, Any]:
        rows = self._connection.execute(
            "SELECT seq,event_id,event_type,event_ts_ns,payload_json,prev_hash,event_hash "
            "FROM events ORDER BY seq",
        ).fetchall()
        previous = GENESIS_HASH
        expected_seq = 1
        for row in rows:
            seq, event_id, event_type, event_ts_ns, payload_json, prev_hash, event_hash = row
            if int(seq) != expected_seq:
                raise JournalIntegrityError(f"event sequence gap: expected {expected_seq}, got {seq}")
            if prev_hash != previous:
                raise JournalIntegrityError(f"event {event_id!r} previous hash mismatch")
            try:
                event_json = canonical_bytes(json.loads(payload_json), schema=EVENT_SCHEMA)
            except Exception as exc:
                raise JournalIntegrityError(f"event {event_id!r} payload is not canonical JSON") from exc
            if _event_hash(previous, event_json) != event_hash:
                raise JournalIntegrityError(f"event {event_id!r} hash mismatch")
            previous = event_hash
            expected_seq += 1
        return {
            "event_count": len(rows),
            "last_seq": expected_seq - 1,
            "last_hash": previous,
        }
