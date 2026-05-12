# ---------------------------------------
# Risk Index Calculation
# ---------------------------------------

def calculate_risk_index(features):
    """
    RiskIndex = Σ (PenaltyWeight × ViolationSeverity) + DriverHistoryFactor
    """

    # Define penalty weights (can be moved to DB later)
    penalty_weights = {
        "violation_severity": 2.0,
        "fine_amount": 0.01,
        "past_violations": 1.5,
        "accident_history": 2.5
    }

    # Compute weighted sum
    risk_index = (
        penalty_weights["violation_severity"] * features["violation_severity"] +
        penalty_weights["fine_amount"] * features["fine_amount"] +
        penalty_weights["past_violations"] * features["past_violations"] +
        penalty_weights["accident_history"] * features["accident_history"]
    )

    return round(risk_index, 2)


# ---------------------------------------
# Decision Logic
# ---------------------------------------

def generate_recommendation(success_probability, risk_index):
    """
    Decide whether to PAY or CONTEST
    """

    if success_probability >= 0.6 and risk_index < 7:
        return "Contest Ticket"
    elif success_probability < 0.4 or risk_index >= 10:
        return "Pay Fine"
    else:
        return "Consider Contesting"


# ---------------------------------------
# Explanation Generator
# ---------------------------------------

def generate_explanation(success_probability, risk_index, features):
    """
    Generate simple explanation for user
    """

    explanation = []

    # Success probability explanation
    if success_probability >= 0.6:
        explanation.append("High chance of winning the dispute.")
    elif success_probability < 0.4:
        explanation.append("Low chance of winning the dispute.")
    else:
        explanation.append("Moderate chance of winning.")

    # Risk explanation
    if risk_index >= 10:
        explanation.append("High risk due to violation severity or history.")
    elif risk_index < 5:
        explanation.append("Low risk based on current data.")
    else:
        explanation.append("Moderate risk level.")

    # Driver history factor
    if features["past_violations"] > 3:
        explanation.append("Multiple past violations reduce success chances.")

    if features["accident_history"] > 1:
        explanation.append("Accident history increases risk.")

    return " ".join(explanation)