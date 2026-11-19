from hypothesis import given, strategies as st
from loan_eligibility import parse_income, monthly_emi, pan_category, CATEGORIES

# Mix of text, None and other wrong types
anything = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(), st.binary()
)


# ---------- No-crash tests (one per function) ----------

@given(st.text() | st.none())
def test_parse_income_no_crash(s):
    try:
        parse_income(s)
    except Exception as e:
        assert False, f"parse_income crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_monthly_emi_no_crash(s):
    try:
        monthly_emi(s)
    except Exception as e:
        assert False, f"monthly_emi crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_pan_category_no_crash(s):
    try:
        pan_category(s)
    except Exception as e:
        assert False, f"pan_category crashed with: {e!r} on input {s!r}"


# ---------- Wrong-type inputs ----------

@given(anything)
def test_all_functions_handle_any_type(x):
    for func in (parse_income, monthly_emi, pan_category):
        try:
            func(x)
        except Exception as e:
            assert False, f"{func.__name__} crashed with: {e!r} on input {x!r}"


# ---------- Property tests on valid inputs ----------

@given(st.integers(min_value=0, max_value=10**12))
def test_parse_income_roundtrip(n):
    assert parse_income(f"{n:,}") == n


@given(
    st.integers(min_value=1000, max_value=10**9),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=1, max_value=50),
)
def test_monthly_emi_valid_inputs(principal, rate, years):
    emi = monthly_emi(f"{principal},{rate},{years}")
    assert emi is not None
    assert emi > 0
    # EMI is rounded to 2 decimals, so each payment can be off by up to 0.005
    n = years * 12
    assert emi * n >= principal - 0.005 * n


@given(
    st.integers(min_value=-(10**6), max_value=10**6),
    st.integers(min_value=-(10**6), max_value=10**6),
    st.integers(min_value=-(10**6), max_value=10**6),
)
def test_monthly_emi_arbitrary_numbers_no_crash(p, r, y):
    try:
        monthly_emi(f"{p},{r},{y}")
    except Exception as e:
        assert False, f"monthly_emi crashed with: {e!r} on {p},{r},{y}"


@given(
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=3, max_size=3),
    st.sampled_from(sorted(CATEGORIES)),
    st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    st.integers(min_value=0, max_value=9999),
    st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
)
def test_pan_category_valid_pan(prefix, cat, fifth, digits, last):
    pan = f"{prefix}{cat}{fifth}{digits:04d}{last}"
    assert pan_category(pan) == CATEGORIES[cat]