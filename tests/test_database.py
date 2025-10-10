import sqlite3
import pytest

from rolodex import init_db, add_person, search_people


@pytest.fixture
def connection():
    """Creates a temporary in-memory SQLite DB for each test"""
    conn = init_db(":memory:")
    yield conn
    conn.close()


def test_add_and_search_person(connection):
    # Add a person with minimal fields
    add_person(
        connection,
        full_name="Alice Smith",
        title="Engineer",
        notes="Loves Python",
    )

    rows = search_people(connection, "Alice Smith")
    assert isinstance(rows, list)
    assert len(rows) == 1
    row = rows[0]
    # row: (id, full_name, title, birthday, tags)
    assert row[1] == "Alice Smith"
    assert row[2] == "Engineer"
    assert row[3] is None or row[3] == ""


def test_search_person_not_found(connection):
    rows = search_people(connection, "Nobody")
    assert rows == []
