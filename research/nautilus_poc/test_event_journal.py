import json
import sqlite3
import subprocess
import sys

import pytest

from pathlib import Path

from event_journal import (
    EventConflictError,
    EventJournal,
    JournalIntegrityError,
    SchemaVersionError,
)


def sample_state():
    return {
        "account": {"currency": "USDT", "balance": "10000.00"},
        "positions": [{"instrument": "BTCUSDT-PERP.BINANCE", "quantity": "0.100"}],
    }


def test_append_is_durable_across_close_and_reopen(tmp_path):
    path = tmp_path / "journal.sqlite"
    with EventJournal(path) as journal:
        first = journal.append_event(
            event_id="evt-1",
            event_type="OrderFilled",
            event_ts_ns=100,
            payload={"price": "40001.0", "quantity": "0.100"},
        )
        journal.append_event(
            event_id="evt-2",
            event_type="FundingSettled",
            event_ts_ns=200,
            payload={"amount": "-0.40", "currency": "USDT"},
        )
        expected = journal.verify_chain()

    with EventJournal(path) as reopened:
        actual = reopened.verify_chain()
        records = reopened.events_after(0)

    assert actual == expected
    assert actual["event_count"] == 2
    assert [record.event_id for record in records] == ["evt-1", "evt-2"]
    assert first.seq == 1


def test_duplicate_event_id_is_idempotent_but_conflicting_payload_is_rejected(tmp_path):
    with EventJournal(tmp_path / "journal.sqlite") as journal:
        first = journal.append_event(
            event_id="fill-1",
            event_type="OrderFilled",
            event_ts_ns=100,
            payload={"price": "40001.0"},
        )
        repeated = journal.append_event(
            event_id="fill-1",
            event_type="OrderFilled",
            event_ts_ns=100,
            payload={"price": "40001.0"},
        )

        assert repeated == first
        assert journal.verify_chain()["event_count"] == 1

        with pytest.raises(EventConflictError, match="different content"):
            journal.append_event(
                event_id="fill-1",
                event_type="OrderFilled",
                event_ts_ns=100,
                payload={"price": "40002.0"},
            )
        assert journal.verify_chain()["event_count"] == 1


def test_hash_chain_detects_event_payload_tampering(tmp_path):
    path = tmp_path / "journal.sqlite"
    with EventJournal(path) as journal:
        journal.append_event(
            event_id="evt-1",
            event_type="OrderFilled",
            event_ts_ns=100,
            payload={"price": "40001.0"},
        )

    with sqlite3.connect(path) as connection:
        connection.execute(
            "UPDATE events SET payload_json=? WHERE event_id=?",
            ('{"schema":"ideal-event/v1","event_id":"evt-1","event_type":"OrderFilled","event_ts_ns":100,"payload":{"price":"99999.0"}}', "evt-1"),
        )

    with EventJournal(path) as reopened:
        with pytest.raises(JournalIntegrityError, match="hash mismatch"):
            reopened.verify_chain()


def test_snapshot_checkpoint_and_post_snapshot_replay_survive_restart(tmp_path):
    path = tmp_path / "journal.sqlite"
    with EventJournal(path) as journal:
        journal.append_event(
            event_id="evt-1",
            event_type="OrderFilled",
            event_ts_ns=100,
            payload={"price": "40001.0"},
        )
        snapshot = journal.create_snapshot(
            snapshot_id="checkpoint-1",
            state=sample_state(),
            created_at_ns=110,
        )
        journal.append_event(
            event_id="evt-2",
            event_type="FundingSettled",
            event_ts_ns=200,
            payload={"amount": "-0.40", "currency": "USDT"},
        )

    with EventJournal(path) as reopened:
        restored = reopened.load_snapshot("checkpoint-1")
        tail = reopened.events_after(restored.through_seq)

    assert restored.state == sample_state()
    assert restored.through_seq == snapshot.through_seq == 1
    assert [event.event_id for event in tail] == ["evt-2"]


def test_snapshot_rejects_corrupted_state_or_chain_anchor(tmp_path):
    path = tmp_path / "journal.sqlite"
    with EventJournal(path) as journal:
        journal.append_event(
            event_id="evt-1",
            event_type="OrderFilled",
            event_ts_ns=100,
            payload={"price": "40001.0"},
        )
        journal.create_snapshot(
            snapshot_id="checkpoint-1",
            state=sample_state(),
            created_at_ns=110,
        )

    with sqlite3.connect(path) as connection:
        connection.execute(
            "UPDATE snapshots SET chain_hash=? WHERE snapshot_id=?",
            ("sha256:" + "f" * 64, "checkpoint-1"),
        )

    with EventJournal(path) as reopened:
        with pytest.raises(JournalIntegrityError, match="chain anchor mismatch"):
            reopened.load_snapshot("checkpoint-1")


def test_journal_rejects_float_payloads(tmp_path):
    with EventJournal(tmp_path / "journal.sqlite") as journal:
        with pytest.raises(TypeError, match="floating-point values are not canonical"):
            journal.append_event(
                event_id="evt-1",
                event_type="OrderFilled",
                event_ts_ns=100,
                payload={"price": 40001.0},
            )
        assert journal.verify_chain()["event_count"] == 0


def test_schema_version_newer_than_code_is_rejected(tmp_path):
    path = tmp_path / "journal.sqlite"
    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA user_version=99")

    with pytest.raises(SchemaVersionError, match="newer than supported"):
        EventJournal(path)



def test_committed_event_survives_abrupt_writer_process_exit(tmp_path):
    path = tmp_path / "crash-recovery.sqlite"
    script = """
import os
import sys
from event_journal import EventJournal

journal = EventJournal(sys.argv[1])
journal.append_event(
    event_id="committed-before-crash",
    event_type="OrderFilled",
    event_ts_ns=123,
    payload={"price": "40001.0"},
)
os._exit(0)
"""
    subprocess.run(
        [sys.executable, "-c", script, str(path)],
        cwd=Path(__file__).parent,
        check=True,
    )

    with EventJournal(path) as recovered:
        verified = recovered.verify_chain()
        records = recovered.events_after(0)

    assert verified["event_count"] == 1
    assert records[0].event_id == "committed-before-crash"



def test_hash_chain_detects_event_metadata_column_tampering(tmp_path):
    path = tmp_path / "journal.sqlite"
    with EventJournal(path) as journal:
        journal.append_event(
            event_id="evt-1",
            event_type="OrderFilled",
            event_ts_ns=100,
            payload={"price": "40001.0"},
        )

    with sqlite3.connect(path) as connection:
        connection.execute(
            "UPDATE events SET event_ts_ns=? WHERE event_id=?",
            (101, "evt-1"),
        )

    with EventJournal(path) as reopened:
        with pytest.raises(JournalIntegrityError, match="columns disagree"):
            reopened.verify_chain()


def test_snapshot_state_tampering_is_detected(tmp_path):
    path = tmp_path / "journal.sqlite"
    with EventJournal(path) as journal:
        journal.append_event(
            event_id="evt-1",
            event_type="OrderFilled",
            event_ts_ns=100,
            payload={"price": "40001.0"},
        )
        journal.create_snapshot(
            snapshot_id="checkpoint-1",
            state=sample_state(),
            created_at_ns=110,
        )

    with sqlite3.connect(path) as connection:
        connection.execute(
            "UPDATE snapshots SET state_json=? WHERE snapshot_id=?",
            ('{"schema":"ideal-state-snapshot/v1","state":{"account":{"balance":"1.00","currency":"USDT"},"positions":[]}}', "checkpoint-1"),
        )

    with EventJournal(path) as reopened:
        with pytest.raises(JournalIntegrityError, match="state hash mismatch"):
            reopened.load_snapshot("checkpoint-1")
