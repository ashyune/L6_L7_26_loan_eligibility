import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


# CREDIT BAND BRANCH TESTS
def test_invalid_score_below_range():
    with pytest.raises(ValueError):
        credit_band(299)

def test_invalid_score_above_range():
    with pytest.raises(ValueError):
        credit_band(901)

def test_boundary_scores():
    assert credit_band(300) == "poor"
    assert credit_band(900) == "excellent"

def test_excellent_band():
    assert credit_band(750) == "excellent"

def test_good_band():
    assert credit_band(650) == "good"

def test_fair_band():
    assert credit_band(550) == "fair"

def test_poor_band():
    assert credit_band(549) == "poor"


# LOAN ELIGIBILITY BRANCH TESTS
def test_unknown_employment():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "unemployed", 800)

def test_age_below_limit():
    assert is_eligible(20, 50000, "salaried", 800) is False

def test_age_above_limit():
    assert is_eligible(61, 50000, "salaried", 800) is False

def test_boundary_ages():
    assert is_eligible(21, 50000, "salaried", 800) is True
    assert is_eligible(60, 50000, "salaried", 800) is True

def test_insufficient_income():
    assert is_eligible(30, 24999, "salaried", 800) is False
    assert is_eligible(30, 39999, "self_employed", 800) is False

def test_minimum_income():
    assert is_eligible(30, 25000, "salaried", 800) is True
    assert is_eligible(30, 40000, "self_employed", 800) is True

def test_poor_credit():
    assert is_eligible(30, 50000, "salaried", 549) is False

def test_eligible_with_good_credit():
    assert is_eligible(30, 50000, "salaried", 650) is True


# INTEREST RATE BRANCH TESTS
def test_excellent_rate():
    assert interest_rate(800, "salaried", False) == 8

def test_good_rate():
    assert interest_rate(700, "salaried", False) == 10

def test_other_credit_band_rate():
    assert interest_rate(600, "salaried", False) == 13

def test_self_employed_addition():
    assert interest_rate(800, "self_employed", False) == 9

def test_collateral_deduction():
    assert interest_rate(800, "salaried", True) == 6

def test_self_employed_with_collateral():
    assert interest_rate(700, "self_employed", True) == 9
