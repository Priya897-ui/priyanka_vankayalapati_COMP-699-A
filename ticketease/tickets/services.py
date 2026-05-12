import re


# ---------------------------------------
# Simulated OCR Extraction
# ---------------------------------------
def extract_ticket_data(form_data):
    """
    Simulates OCR extraction from user input
    """

    extracted_text = f"""
    Violation: {form_data.get('violation_type')}
    Location: {form_data.get('location')}
    Fine: {form_data.get('fine_amount')}
    Date: {form_data.get('ticket_date')}
    """

    return {
        "violation_type": form_data.get("violation_type"),
        "location": form_data.get("location"),
        "fine_amount": float(form_data.get("fine_amount")),
        "ticket_date": form_data.get("ticket_date"),
        "extracted_text": extracted_text.strip()
    }


# ---------------------------------------
# Text Cleaning & Preprocessing
# ---------------------------------------
def clean_text(text):
    """
    Basic text cleaning
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)   # remove extra spaces
    text = re.sub(r'[^a-z0-9\s:]', '', text)  # remove special chars
    return text.strip()


# ---------------------------------------
# Feature Engineering
# ---------------------------------------
def prepare_features(ticket_data, driver_profile):
    """
    Convert ticket + driver info into ML-ready features
    """

    # Map violation types to severity
    severity_map = {
        "speeding": 3,
        "parking": 1,
        "signal violation": 4,
        "no helmet": 2,
        "other": 1
    }

    violation = ticket_data.get("violation_type", "").lower()

    violation_severity = severity_map.get(violation, 1)

    fine_amount = float(ticket_data.get("fine_amount", 0))

    # Driver history factors
    past_violations = driver_profile.past_violations
    accident_history = driver_profile.accident_history

    # Feature vector
    features = {
        "violation_severity": violation_severity,
        "fine_amount": fine_amount,
        "past_violations": past_violations,
        "accident_history": accident_history
    }

    return features


# ---------------------------------------
# Utility: Normalize Data
# ---------------------------------------
def normalize_features(features):
    """
    Normalize numeric values (simple scaling)
    """

    normalized = {
        "violation_severity": features["violation_severity"] / 5,
        "fine_amount": features["fine_amount"] / 10000,
        "past_violations": features["past_violations"] / 10,
        "accident_history": features["accident_history"] / 5
    }

    return normalized