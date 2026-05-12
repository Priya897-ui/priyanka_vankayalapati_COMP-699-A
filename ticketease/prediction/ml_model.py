import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier


class TicketPredictionModel:
    """
    Simulated Random Forest Model for Ticket Outcome Prediction
    """

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=20, random_state=42)
        self.is_trained = False

    # ---------------------------------------
    # Train Model (using balanced dummy data)
    # ---------------------------------------
    def train_model(self):
        """
        Train model using synthetic balanced data
        """

        X = []
        y = []

        for _ in range(300):
            violation_severity = random.randint(1, 5)
            fine_amount = random.randint(100, 5000)
            past_violations = random.randint(0, 10)
            accident_history = random.randint(0, 5)

            score = (
                violation_severity * 2 +
                fine_amount * 0.001 +
                past_violations * 1.5 +
                accident_history * 2
            )

            # Balanced logic
            if score < 8:
                label = 1  # success
            else:
                label = 0  # failure

            X.append([
                violation_severity,
                fine_amount,
                past_violations,
                accident_history
            ])
            y.append(label)

        X = np.array(X)
        y = np.array(y)

        self.model.fit(X, y)
        self.is_trained = True

    # ---------------------------------------
    # Predict Probability (SAFE VERSION)
    # ---------------------------------------
    def predict_success_probability(self, features):
        """
        Predict probability of successful dispute
        """

        if not self.is_trained:
            self.train_model()

        input_data = np.array([[
            features["violation_severity"],
            features["fine_amount"],
            features["past_violations"],
            features["accident_history"]
        ]])

        probabilities = self.model.predict_proba(input_data)[0]

        # ✅ CRITICAL FIX (prevents crash)
        if len(probabilities) == 1:
            prob = probabilities[0]
        else:
            prob = probabilities[1]

        return round(float(prob), 2)


# ---------------------------------------
# Singleton instance (global model)
# ---------------------------------------
model_instance = TicketPredictionModel()


# ---------------------------------------
# Helper function (used in views)
# ---------------------------------------
def get_prediction(features):
    """
    Main function to get prediction output
    """
    return model_instance.predict_success_probability(features)