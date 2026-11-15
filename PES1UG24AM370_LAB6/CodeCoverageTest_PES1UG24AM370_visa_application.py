"""Lab 6 - Code (line) coverage tests for visa_application.py
SRN: PES1UG24AM370

Run:
    coverage run -m pytest CodeCoverageTest_PES1UG24AM370_visa_application.py
    coverage report -m
"""
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ---------------- visa_fee ----------------
def test_within_included_entries():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_unknown_visa_type_raises():
    with pytest.raises(ValueError):
        visa_fee("diplomatic", 1, "normal", "B")


def test_negative_entries_raises():
    with pytest.raises(ValueError):
        visa_fee("tourist", -1, "normal", "B")


def test_group_a_bonus_entry_included():
    # business (3) + 1 bonus = 4 included, so 4 entries are free
    assert visa_fee("business", 4, "normal", "A") == 0


def test_normal_speed_extra_entries():
    # tourist includes 1; 3 entries -> 2 extra * 40
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_express_speed_extra_entries():
    # 2 extra * 100
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_normal_large_extra_surcharge():
    # 6 extra * (40 + 20)
    assert visa_fee("tourist", 7, "normal", "B") == 360


def test_express_large_extra_surcharge():
    # 6 extra * (100 + 20 + 10)
    assert visa_fee("tourist", 7, "express", "B") == 780


# ---------------- documents_complete ----------------
def test_documents_complete():
    assert documents_complete(3, 2, False) is True


def test_renewal_needs_one_form():
    assert documents_complete(1, 0, True) is True


def test_too_few_photos():
    assert documents_complete(3, 1, False) is False


def test_too_few_forms():
    assert documents_complete(2, 2, False) is False


# ---------------- application_status ----------------
def test_status_open():
    assert application_status(30, False, False) == "open"


def test_status_closing():
    assert application_status(15, False, False) == "closing"


def test_status_closed():
    assert application_status(0, False, False) == "closed"


def test_status_express_peak_open():
    assert application_status(25, True, True) == "open"
