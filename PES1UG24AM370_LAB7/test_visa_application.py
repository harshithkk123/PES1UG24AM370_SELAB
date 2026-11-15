"""Lab 7 - Hypothesis fuzz tests for visa_application.py
SRN: PES1UG24AM370

Run:  python -m pytest test_visa_application.py
"""
import math
from hypothesis import given, strategies as st
from visa_application import parse_application, processing_average, payable_fee

# Anything at all: text, None, numbers, bytes, lists
anything = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(),
    st.binary(), st.lists(st.integers()),
)


# ---------------- parse_application ----------------
@given(st.text() | st.none())
def test_parse_application_no_crash(s):
    try:
        parse_application(s)
    except Exception as e:
        assert False, f"parse_application crashed with: {e!r} on input {s!r}"


@given(anything)
def test_parse_application_any_type_no_crash(s):
    try:
        parse_application(s)
    except Exception as e:
        assert False, f"parse_application crashed with: {e!r} on input {s!r}"


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1),
       st.integers(min_value=0, max_value=10**6))
def test_parse_application_valid_roundtrip(visa, n):
    result = parse_application(f"{visa}:{n}")
    assert result is not None
    assert result[1] == n
    assert result[0] == visa.strip().title()


# ---------------- processing_average ----------------
@given(st.text() | st.none())
def test_processing_average_no_crash(s):
    try:
        processing_average(s)
    except Exception as e:
        assert False, f"processing_average crashed with: {e!r} on input {s!r}"


@given(anything)
def test_processing_average_any_type_no_crash(s):
    try:
        processing_average(s)
    except Exception as e:
        assert False, f"processing_average crashed with: {e!r} on input {s!r}"


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1))
def test_processing_average_within_min_max(nums):
    result = processing_average(",".join(map(str, nums)))
    assert result is not None
    assert min(nums) <= result <= max(nums)


# ---------------- payable_fee ----------------
@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r} on input {s!r}"


@given(anything)
def test_payable_fee_any_type_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r} on input {s!r}"


@given(st.floats(min_value=0, max_value=1e9, allow_nan=False),
       st.floats(min_value=0, max_value=1e9, allow_nan=False))
def test_payable_fee_never_negative_and_finite(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result is not None
    assert result >= 0 and math.isfinite(result)
