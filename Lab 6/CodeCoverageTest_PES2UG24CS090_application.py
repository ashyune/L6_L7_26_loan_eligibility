import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


# CREDIT BAND TESTS

def test_excellent_band():
    assert credit_band(800) == "excellent"


def test_good_band():
    assert credit_band(700) == "good"


def test_fair_band():
    assert credit_band(600) == "fair"


def test_poor_band():
    assert credit_band(500) == "poor"


def test_invalid_low_score():
    with pytest.raises(ValueError):
        credit_band(200)


def test_invalid_high_score():
    with pytest.raises(ValueError):
        credit_band(950)


# LOAN ELIGIBILITY TESTS

def test_eligible_salaried():
    assert is_eligible(30, 50000, "salaried", 800) is True


def test_eligible_self_employed():
    assert is_eligible(35, 60000, "self_employed", 700) is True


def test_unknown_employment():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "unemployed", 800)


def test_below_minimum_age():
    assert is_eligible(20, 50000, "salaried", 800) is False


def test_above_maximum_age():
    assert is_eligible(61, 50000, "salaried", 800) is False


def test_insufficient_salaried_income():
    assert is_eligible(30, 20000, "salaried", 800) is False


def test_insufficient_self_employed_income():
    assert is_eligible(30, 30000, "self_employed", 800) is False


def test_poor_credit_ineligible():
    assert is_eligible(30, 50000, "salaried", 500) is False


# INTEREST RATE TESTS

def test_excellent_interest_rate():
    assert interest_rate(800, "salaried", False) == 8


def test_good_interest_rate():
    assert interest_rate(700, "salaried", False) == 10


def test_poor_interest_rate():
    assert interest_rate(500, "salaried", False) == 13


def test_self_employed_interest_rate():
    assert interest_rate(800, "self_employed", False) == 9


def test_collateral_interest_rate():
    assert interest_rate(800, "salaried", True) == 6
