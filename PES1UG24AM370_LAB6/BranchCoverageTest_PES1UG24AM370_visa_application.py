"""Lab 6 - Branch coverage tests for visa_application.py
SRN: PES1UG24AM370

Every decision is exercised with both True and False outcomes, including
the exact boundary values (>=, >, <=, <).

Run:
    coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM370_visa_application.py
    coverage report -m
"""
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ======================= visa_fee =======================
# Branch: visa_type not in INCLUDED_ENTRIES (True / False)
def test_within_included_entries():
    assert visa_fee("tourist", 1, "normal", "B") == 0


@pytest.mark.parametrize("bad_type", ["diplomatic", "", "Tourist"])
def test_unknown_visa_type_raises(bad_type):
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee(bad_type, 1, "normal", "B")


# Branch: entries < 0 (True / False) + boundary 0
def test_negative_entries_raises():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_zero_entries_is_free():
    assert visa_fee("tourist", 0, "normal", "B") == 0


# Branch: nationality_group == "A" and visa_type != "student"
def test_group_a_non_student_gets_bonus():
    assert visa_fee("business", 4, "normal", "A") == 0      # 3 + 1 included
    assert visa_fee("business", 5, "normal", "A") == 40     # 1 extra


def test_group_a_student_gets_no_bonus():
    assert visa_fee("student", 3, "normal", "A") == 40      # 2 included only


def test_non_group_a_gets_no_bonus():
    assert visa_fee("business", 4, "normal", "B") == 40     # 3 included only


# Branch: extra <= 0 (True / False) with boundary extra == 0
def test_extra_exactly_zero():
    assert visa_fee("student", 2, "express", "B") == 0


def test_extra_one_is_charged():
    assert visa_fee("student", 3, "express", "B") == 100


# Branch: speed == "express" (rate selection)
def test_normal_rate():
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_express_rate():
    assert visa_fee("tourist", 3, "express", "B") == 200


# Branch: extra > 5 (boundary 5 / 6) and inner express check
def test_extra_five_no_surcharge_normal():
    assert visa_fee("tourist", 6, "normal", "B") == 200     # 5 * 40


def test_extra_five_no_surcharge_express():
    assert visa_fee("tourist", 6, "express", "B") == 500    # 5 * 100


def test_extra_six_surcharge_normal():
    assert visa_fee("tourist", 7, "normal", "B") == 360     # 6 * 60


def test_extra_six_surcharge_express():
    assert visa_fee("tourist", 7, "express", "B") == 780    # 6 * 130


# ================== documents_complete ==================
# Branch: is_renewal (True / False)
def test_renewal_with_one_form():
    assert documents_complete(1, 0, True) is True


def test_renewal_with_no_forms():
    assert documents_complete(0, 5, True) is False


# Branch: photos < 2 (True / False) with boundary
def test_new_application_one_photo():
    assert documents_complete(3, 1, False) is False


def test_new_application_two_photos_enough():
    assert documents_complete(3, 2, False) is True


# forms_filed >= 3 boundary
def test_new_application_two_forms():
    assert documents_complete(2, 2, False) is False


# ================= application_status ===================
# Branch: is_express (True / False)  x  is_peak_season (True / False)
# Branch: days_left >= cutoff, >= cutoff-15, else
@pytest.mark.parametrize(
    "days, express, peak, expected",
    [
        # normal, off-peak: cutoff 30
        (30, False, False, "open"),
        (29, False, False, "closing"),
        (15, False, False, "closing"),
        (14, False, False, "closed"),
        # express, off-peak: cutoff 10
        (10, True, False, "open"),
        (9, True, False, "closing"),
        (-5, True, False, "closing"),
        (-6, True, False, "closed"),
        # normal, peak: cutoff 45
        (45, False, True, "open"),
        (44, False, True, "closing"),
        (30, False, True, "closing"),
        (29, False, True, "closed"),
        # express, peak: cutoff 25
        (25, True, True, "open"),
        (24, True, True, "closing"),
        (10, True, True, "closing"),
        (9, True, True, "closed"),
    ],
)
def test_application_status(days, express, peak, expected):
    assert application_status(days, express, peak) == expected
