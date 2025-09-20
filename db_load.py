import sqlite3
import random
import datetime
from rich.console import Console
from db import init_db, DB_NAME

console = Console()

def make_name(syllable_count=2) -> str:
    syllables = ["an", "bel", "cor", "dan", "el", "fin", "gar", 
                 "han", "iv", "jon", "ka", "lor", "mar", "nel", 
                 "or", "pen", "quin", "ran", "sol", "tor"]
    name = "".join(random.choice(syllables) for _ in range(syllable_count))
    return name.capitalize()

def random_birthday(start_year: int = 1950, end_year: int = 2010) -> datetime.date:
    """Generate a random birthday between start_year and end_year."""

    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    
    # Random number of days between start_date and end_date
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    
    return start_date + datetime.timedelta(days=random_days)

def insert(full_name, birthday, title, address, notes, tags):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO people (full_name, birthday, title, address, notes, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (full_name, birthday, title, address, notes, tags))
        conn.commit()
        console.print("[green]Person added successfully.[/green]")

def main():
    for _ in range(10):
        print(f"{make_name()} {make_name()}, {random_birthday()}")

if __name__ == "__main__":
    main()
