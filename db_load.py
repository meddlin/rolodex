import sqlite3
import random
import datetime
from rich.console import Console
from db import init_db, DB_NAME

console = Console()

def make_name(syllable_count=2) -> str:
    """Generate a random name"""

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

def random_title() -> str:
    """Generate a randomized corporate-sounding job title."""

    prefixes = [
    "Junior", "Senior", "Lead", "Principal", "Assistant",
    "Associate", "Chief", "Global", "Regional", "Head of"
    ]
    roles = [
        "Engineer", "Developer", "Manager", "Analyst",
        "Coordinator", "Director", "Specialist", "Officer",
        "Consultant", "Strategist"
    ]
    domains = [
        "Technology", "Software", "Product", "Operations",
        "Finance", "Marketing", "Human Resources", "Security",
        "Innovation", "Data", "Infrastructure"
    ]

    use_prefix = random.choice([True, False])
    prefix = random.choice(prefixes) if use_prefix else ""
    role = random.choice(roles)
    domain = random.choice(domains)

    parts = [prefix, role, "of", domain] if prefix else [role, "of", domain]
    return " ".join(parts)

def __address_make_word(min_syllables: int = 2, max_syllables: int = 3) -> str:
    """Generate a pseudo-word from syllables."""
    # Shared syllable pool (you can tweak this to change the "flavor")
    syllables = [
        "an", "bel", "cor", "dan", "el", "fin", "gar", "han",
        "iv", "jon", "ka", "lor", "mar", "nel", "or", "pen",
        "quil", "ran", "sol", "tor", "ul", "ven", "wyn", "xer",
        "yor", "zen"
    ]

    count = random.randint(min_syllables, max_syllables)
    word = "".join(random.choice(syllables) for _ in range(count))
    return word.capitalize()

def random_address() -> str:
    """Generate a synthetic but structured U.S.-style mailing address."""

    street_types = ["St", "Ave", "Blvd", "Ln", "Rd", "Dr", "Pl", "Ct", "Way"]

    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "IL", "IN", "IA", "KS", "KY", "LA", "MA", "MD", "ME", "MI",
        "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM",
        "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN",
        "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"
    ]
    
    number = random.randint(100, 9999)
    street_name = __address_make_word() + " " + random.choice(street_types)
    city = __address_make_word(min_syllables=2, max_syllables=4)
    state = random.choice(states)
    zipcode = f"{random.randint(10000, 99999)}"
    return f"{number} {street_name}, {city}, {state} {zipcode}"

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
        full_name = f"{make_name()} {make_name()}"
        birthday = random_birthday()
        title = random_title()
        address = random_address()
        # print(f"{make_name()} {make_name()}, {random_birthday()}, {random_title()}, {random_address()}")
        insert(full_name=full_name, birthday=birthday, title=title, address=address, notes='', tags='')

if __name__ == "__main__":
    main()
