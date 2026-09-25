#!/usr/bin/env python3
"""Apply every migration to real SQLite and verify integrity and TTL cascades."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def expect_constraint(db, sql, parameters=()):
    try:
        db.execute(sql, parameters)
    except sqlite3.IntegrityError:
        return
    raise AssertionError(f"Expected constraint failure: {sql}")


def main():
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys = ON")
    migrations = sorted((ROOT / "migrations").glob("*.sql"))
    assert migrations, "No migrations found"
    for migration in migrations:
        db.executescript(migration.read_text())
    assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
    assert not db.execute("PRAGMA foreign_key_check").fetchall()
    tables = {row[1]: row[5] for row in db.execute("PRAGMA table_list")}
    for name in ["sessions", "issues", "comments", "rate_buckets"]:
        assert tables[name] == 1, f"{name} must be STRICT"
    session = "INSERT INTO sessions VALUES (?, ?, ?, ?, ?)"
    db.execute(session, ("hash", "board", "editor", "2026-01-02", "2026-01-01"))
    db.execute(session, ("hash2", "board2", "viewer", "2026-01-04", "2026-01-01"))
    expect_constraint(db, session, ("bad", "bad", "admin", "2026-01-02", "2026-01-01"))
    issue = "INSERT INTO issues VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    valid_issue = ("i1", "board", "Title", "Description", "high", "triage", "2026-01-01", "2026-01-01")
    db.execute(issue, valid_issue)
    for index, invalid in [(1, "missing"), (2, " "), (2, "x" * 121), (3, "x" * 2001), (4, "urgent"), (5, "closed")]:
        row = list(valid_issue)
        row[0] = "invalid"
        row[index] = invalid
        expect_constraint(db, issue, row)
    db.execute("INSERT INTO comments VALUES ('c1', 'i1', 'Comment', '2026-01-01')")
    expect_constraint(db, "INSERT INTO comments VALUES ('bad', 'missing', 'Text', '2026-01-01')")
    expect_constraint(db, "INSERT INTO comments VALUES ('bad', 'i1', '', '2026-01-01')")
    expect_constraint(db, "INSERT INTO comments VALUES ('bad', 'i1', ?, '2026-01-01')", ("x" * 1001,))
    # Rate bucket upsert admits exactly ten concurrent-safe reservations per key.
    reserve = "INSERT INTO rate_buckets VALUES ('key', 1, '2026-01-02') ON CONFLICT(key) DO UPDATE SET count = count + 1 WHERE count < 10 RETURNING count"
    for expected in range(1, 11):
        assert db.execute(reserve).fetchone() == (expected,)
    assert db.execute(reserve).fetchone() is None
    # Expiration removes only the expired board, cascading all child content.
    db.execute("DELETE FROM sessions WHERE expires_at <= '2026-01-03'")
    assert db.execute("SELECT workspace_id FROM sessions").fetchall() == [("board2",)]
    assert db.execute("SELECT count(*) FROM issues").fetchone() == (0,)
    assert db.execute("SELECT count(*) FROM comments").fetchone() == (0,)
    db.execute("DELETE FROM rate_buckets WHERE expires_at <= '2026-01-03'")
    assert db.execute("SELECT count(*) FROM rate_buckets").fetchone() == (0,)
    assert not db.execute("PRAGMA foreign_key_check").fetchall()
    print(f"PASS: {len(migrations)} migration(s), strict schemas, constraints, rate limit, TTL cascade, integrity")


if __name__ == "__main__":
    main()
