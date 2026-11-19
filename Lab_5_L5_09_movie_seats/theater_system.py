"""Movie theater seat reservation system.

Reserves and releases seats for each show, generates a short ticket code
and saves the seating plan to a JSON file.
"""

import hashlib
import json
import os

SEATS_FILE = "seats.json"

# Global state: show id -> title, seat capacity and booked seat numbers
shows = {
    "SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
    "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []},
}


def _is_valid_seat(show, seat_number):
    """Return True for a whole seat number from 1 up to the capacity."""
    return (
        isinstance(seat_number, int)
        and not isinstance(seat_number, bool)
        and 1 <= seat_number <= show["seats"]
    )


def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve a seat for a show and return True if it was booked.

    Unknown shows, invalid seat numbers and seats that are already taken
    are rejected. Every outcome is appended to system_logs if a list is
    given.
    """
    if system_logs is None:
        system_logs = []
    show = shows.get(show_id)
    if show is None:
        system_logs.append(f"Unknown show {show_id}")
        return False
    if not _is_valid_seat(show, seat_number):
        system_logs.append(f"Invalid seat {seat_number!r} for {show_id}")
        return False
    if seat_number in show["booked"]:
        system_logs.append(f"Seat {seat_number} already taken for {show_id}")
        return False
    show["booked"].append(seat_number)
    system_logs.append(f"Reserved seat {seat_number} for {show_id}")
    return True


def release_seat(show_id, seat_number):
    """Release a booked seat and return True if it had been booked."""
    show = shows.get(show_id)
    if show is None or seat_number not in show["booked"]:
        return False
    show["booked"].remove(seat_number)
    return True


def ticket_code(show_id, seat_number):
    """Return an 8-character code identifying one seat for one show."""
    raw = f"{show_id}:{seat_number}".encode()
    return hashlib.sha256(raw).hexdigest()[:8]


def dump_reservations(path=SEATS_FILE):
    """Save the seating plan to a JSON file only the owner can access."""
    with open(path, "w", encoding="utf-8") as seats_file:
        json.dump(shows, seats_file)
    os.chmod(path, 0o600)


def load_reservations(path=SEATS_FILE):
    """Replace the in-memory seating plan with the one saved in a file."""
    with open(path, encoding="utf-8") as seats_file:
        data = json.load(seats_file)
    shows.clear()
    shows.update(data)


def print_seating_summary():
    """Print the free seat count and booked seats for every show."""
    for show in shows.values():
        free = show["seats"] - len(show["booked"])
        print(f"{show['title']}: {free} seats free, "
              f"booked = {show['booked']}")


def parse_seat(text):
    """Convert user input to a seat number, or None if it is not a number."""
    try:
        return int(text)
    except ValueError:
        return None


def main():
    """Run the demo bookings, ask for one more seat and show the summary."""
    logs = []
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 25, logs)
    reserve_seat("SHOW-2", -1, logs)
    reserve_seat("SHOW-2", "A7", logs)
    release_seat("SHOW-2", 3)
    print("Ticket code:", ticket_code("SHOW-1", 5))
    choice = input("Seat number to book for SHOW-2 (Enter for 4): ") or "4"
    seat = parse_seat(choice)
    if seat is None:
        logs.append(f"Invalid seat input {choice!r}")
    else:
        reserve_seat("SHOW-2", seat, logs)
    dump_reservations()
    load_reservations()
    print_seating_summary()
    print("Log:")
    for entry in logs:
        print(" -", entry)


if __name__ == "__main__":
    main()
