import re

CATEGORIES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}

# Sanity limits so absurd inputs can't cause overflow or nonsense results
MAX_INCOME_DIGITS = 15
MAX_PRINCIPAL = 10**12
MAX_RATE = 100      # percent per year
MAX_YEARS = 50

PAN_PATTERN = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")


def parse_income(income):
    """Parse a string like '50,000' into an int.
    Returns None for invalid input (wrong type, empty, negative, non-numeric)."""
    if not isinstance(income, str):
        return None
    cleaned = income.strip().replace(",", "")
    if not cleaned.isascii() or not cleaned.isdigit():
        return None
    if len(cleaned) > MAX_INCOME_DIGITS:
        return None
    return int(cleaned)


def monthly_emi(details):
    """Compute EMI from 'principal,rate,years'.
    Returns None for invalid input or out-of-range values."""
    if not isinstance(details, str):
        return None

    parts = details.split(",")
    if len(parts) != 3:
        return None

    try:
        principal, rate, years = (int(p) for p in parts)
    except ValueError:
        return None

    if not (0 < principal <= MAX_PRINCIPAL
            and 0 <= rate <= MAX_RATE
            and 0 < years <= MAX_YEARS):
        return None

    r = rate / 1200
    n = years * 12

    try:
        if r == 0:  # interest-free loan: avoid division by zero
            emi = principal / n
        else:
            growth = (1 + r) ** n
            emi = principal * r * growth / (growth - 1)
    except (OverflowError, ZeroDivisionError):
        return None

    return round(emi, 2)


def pan_category(pan):
    """Return the holder category from a PAN's 4th character.
    Returns None for invalid PANs."""
    if not isinstance(pan, str):
        return None
    pan = pan.strip()
    if not pan.isascii():
        return None
    pan = pan.upper()
    if not PAN_PATTERN.fullmatch(pan):
        return None
    return CATEGORIES.get(pan[3])


def main():
    print("==== Running parse_income ====")
    user_input = input("Enter monthly income (e.g. 50,000): ")
    result = parse_income(user_input)
    print("Income:", result if result is not None else "Invalid input")

    print("\n==== Running monthly_emi ====")
    user_input = input("Enter principal,rate,years (e.g. 500000,10,5): ")
    result = monthly_emi(user_input)
    print("Monthly EMI:", result if result is not None else "Invalid input")

    print("\n==== Running pan_category ====")
    user_input = input("Enter a PAN number (e.g. ABCPE1234F): ")
    result = pan_category(user_input)
    print("PAN Category:", result if result is not None else "Invalid PAN")


if __name__ == "__main__":
    main()