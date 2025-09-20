import argparse
import sqlite3
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from db import init_db, DB_NAME

console = Console()

def add_person(full_name, birthday, title, address, notes, tags):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO people (full_name, birthday, title, address, notes, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (full_name, birthday, title, address, notes, tags))
        conn.commit()
        console.print("[green]Person added successfully.[/green]")

def list_people():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, full_name, title, birthday, tags, notes FROM people")
        rows = c.fetchall()

    if rows:
        table = Table(title="People in CRM")
        table.add_column("ID", justify="right")
        table.add_column("Name")
        table.add_column("Title")
        table.add_column("Birthday")
        table.add_column("Tags")
        table.add_column("Notes")

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3], row[4], row[5] or "")
        console.print(table)
    else:
        console.print("[yellow]No people found.[/yellow]")

def search_people(name_query):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, full_name, title, birthday, tags FROM people WHERE full_name LIKE ?", (f"%{name_query}%",))
        rows = c.fetchall()

    if rows:
        table = Table(title=f"Search Results for '{name_query}'")
        table.add_column("ID", justify="right")
        table.add_column("Name")
        table.add_column("Title")
        table.add_column("Birthday")
        table.add_column("Tags")

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3], row[4] or "")
        console.print(table)
    else:
        console.print(f"[red]No results found for '{name_query}'.[/red]")

def show_notes(person_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT full_name, notes FROM people WHERE id = ?", (person_id,))
        row = c.fetchone()

    if row:
        console.print(f"[bold underline]{row[0]}'s Notes:[/bold underline]")
        console.print(Markdown(row[1]))
    else:
        console.print("[red]No notes found for that person ID.[/red]")

def delete_person(person_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM people WHERE id = ?", (person_id,))
        conn.commit()
        console.print(f"[red]Deleted person with ID {person_id}.[/red]")

def edit_person(person_id, **fields):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        updates = ", ".join(f"{key} = ?" for key in fields if fields[key] is not None)
        values = [fields[key] for key in fields if fields[key] is not None]
        values.append(person_id)
        c.execute(f"UPDATE people SET {updates} WHERE id = ?", values)
        conn.commit()
        console.print(f"[cyan]Updated person with ID {person_id}.[/cyan]")

def main():
    parser = argparse.ArgumentParser(description="Personal CRM CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add
    add = subparsers.add_parser("add", help="Add a new person")
    add.add_argument("full_name")
    add.add_argument("--birthday", default="")
    add.add_argument("--title", default="")
    add.add_argument("--address", default="")
    add.add_argument("--notes", default="")
    add.add_argument("--tags", default="")

    # List
    subparsers.add_parser("list", help="List all people")

    # Search
    search = subparsers.add_parser("search", help="Search people by name")
    search.add_argument("query")

    # Notes
    notes = subparsers.add_parser("notes", help="View notes (Markdown rendered) by person ID")
    notes.add_argument("id", type=int)

    # Delete
    delete = subparsers.add_parser("delete", help="Delete a person by ID")
    delete.add_argument("id", type=int)

    # Edit
    edit = subparsers.add_parser("edit", help="Edit a person by ID")
    edit.add_argument("id", type=int)
    edit.add_argument("--full_name")
    edit.add_argument("--birthday")
    edit.add_argument("--title")
    edit.add_argument("--address")
    edit.add_argument("--notes")
    edit.add_argument("--tags")

    args = parser.parse_args()
    init_db()

    if args.command == "add":
        add_person(args.full_name, args.birthday, args.title, args.address, args.notes, args.tags)
    elif args.command == "list":
        list_people()
    elif args.command == "search":
        search_people(args.query)
    elif args.command == "notes":
        show_notes(args.id)
    elif args.command == "delete":
        delete_person(args.id)
    elif args.command == "edit":
        edit_person(args.id,
                    full_name=args.full_name,
                    birthday=args.birthday,
                    title=args.title,
                    address=args.address,
                    notes=args.notes,
                    tags=args.tags)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
