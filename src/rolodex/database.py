from typing import List, Optional, Sequence, Tuple
import sqlite3
from rich.console import Console
from rich.table import Table


DB_NAME = "database.db"
console = Console()


def search_people(conn: sqlite3.Connection, name_query: str) -> Sequence[Tuple]:
    """Search people by partial full_name match.

    Returns a sequence of rows with columns:
    (id, full_name, title, birthday, tags)
    """
    cursor = conn.execute(
        "SELECT id, full_name, title, birthday, tags FROM people WHERE full_name LIKE ?",
        (f"%{name_query}%",),
    )
    rows = cursor.fetchall()

    if rows:
        table = Table(title=f"Search Results for '{name_query}'")
        table.add_column("ID", justify="right")
        table.add_column("Name")
        table.add_column("Title")
        table.add_column("Birthday")
        table.add_column("Tags")

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2] or "", row[3] or "", row[4] or "")
        console.print(table)
    else:
        console.print(f"[red]No results found for '{name_query}'.[/red]")

    return rows


def add_person(
        conn: sqlite3.Connection,
        full_name: Optional[str] = None,
        birthday: Optional[str] = None,
        title: Optional[str] = None,
        address: Optional[str] = None,
        notes: Optional[str] = None,
        tags: Optional[str] = None
    ) -> None:
    """Insert a new person into the database."""

    conn.execute('''
        INSERT INTO people (full_name, birthday, title, address, notes, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (full_name, birthday, title, address, notes, tags))
    conn.commit()
    console.print("[green]Person added successfully.[/green]")


def init_db(db_name: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                birthday TEXT,
                title TEXT,
                address TEXT,
                notes TEXT,
                tags TEXT
            )
        ''')
    return conn
