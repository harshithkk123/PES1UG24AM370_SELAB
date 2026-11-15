"""Lab 7 - Fixed (hardened) visa_application.py
SRN: PES1UG24AM370

Every function now validates its input and returns None for anything
invalid (wrong type, missing/extra separators, empty parts, non-numeric,
negative, NaN/inf, ...) instead of raising an exception.
"""
import math


def _to_int(part):
    """Return a non-negative int from a string like ' 12 ', else None."""
    if not isinstance(part, str):
        return None
    part = part.strip()
    if not part.isdecimal():          # rejects '', '-1', '1.5', '1_0', '²'
        return None
    try:
        return int(part)
    except ValueError:                # e.g. absurdly long digit strings
        return None


def _to_float(part):
    """Return a finite, non-negative float from a string, else None."""
    if not isinstance(part, str):
        return None
    try:
        value = float(part.strip())
    except ValueError:
        return None
    if not math.isfinite(value) or value < 0:   # rejects nan, inf, negatives
        return None
    return value


def parse_application(text):
    """'tourist:2' -> ('Tourist', 2).  Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:               # no colon, or more than one colon
        return None
    visa = parts[0].strip()
    entries = _to_int(parts[1])
    if not visa or entries is None:
        return None
    return visa.title(), entries


def processing_average(days_csv):
    """'5,10,21' -> 12 (integer average).  Returns None for invalid input."""
    if not isinstance(days_csv, str):
        return None
    values = [_to_int(r) for r in days_csv.split(',')]
    if not values or any(v is None for v in values):   # empty / bad element
        return None
    return sum(values) // len(values)


def payable_fee(text):
    """'6000|500' -> fee*1.18 - discount, never below 0.  None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    fee = _to_float(parts[0])
    discount = _to_float(parts[1])
    if fee is None or discount is None:
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):      # fee so large that it overflows
        return None
    return max(total, 0)


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:",
          result if result is not None else "Invalid input")

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:",
          result if result is not None else "Invalid input")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
