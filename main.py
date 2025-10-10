import argparse
import sqlite3
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rolodex import init_db, DB_NAME, MarkdownEditor, add_person, search_people

console = Console()



def list_people():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, full_name, title, birthday, tags, notes FROM people")
        rows = c.fetchall()

    if rows:
        table = Table(title="People")
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

def get_person_by_id(conn, person_id: int):
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, notes FROM people WHERE id=?", (person_id,))
    return cur.fetchone()


def update_notes(conn, person_id: int, notes: str):
    cur = conn.cursor()
    cur.execute("UPDATE people SET notes=? WHERE id=?", (notes, person_id))
    conn.commit()


def edit_notes(person_id: int):
    conn = sqlite3.connect(DB_NAME)
    row = get_person_by_id(conn, person_id)
    if not row:
        print(f"No person with ID {person_id}")
        return
    _id, name, notes = row
    print(f"Editing notes for {name}... (Ctrl+S to save, Ctrl+Q to quit)")

    def save_callback(new_text: str):
        update_notes(conn, person_id, new_text)
        print(f"Notes saved for {name}!")

    MarkdownEditor(initial_text=notes or "", on_save=save_callback).run()
    conn.close()

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
    notes.add_argument("--id", type=int)

    edit_cmd = subparsers.add_parser("edit-notes", help="Edit notes for a person in your default editor")
    edit_cmd.add_argument("--id", type=int, required=True)

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
    conn = init_db(DB_NAME)
    conn.close()

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
    elif args.command == "edit-notes":
        edit_notes(args.id)
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
