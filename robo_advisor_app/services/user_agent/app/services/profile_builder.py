class ProfileBuilder:

    def __init__(self):
        pass

    def _score_risk(self, answers):
        score = 50

        # Horizon
        if answers["horizon"] >= 10:
            score += 20
        elif answers["horizon"] <= 3:
            score -= 15

        # Risk preference
        score += {
            "low": -20,
            "medium": 0,
            "high": 20
        }[answers["risk_preference"]]

        # Market reaction
        score += {
            "panic": -30,
            "concerned": -10,
            "hold": 5,
            "buy_more": 15
        }[answers["market_reaction"]]

        # Experience
        score += {
            "beginner": -10,
            "intermediate": 0,
            "advanced": 10
        }[answers["experience"]]

        # Liquidity
        score += {
            "high": -20,
            "medium": -5,
            "low": 10
        }[answers["liquidity_need"]]

        # clamp
        return max(0, min(100, score))

    def _risk_category(self, score):
        if score < 30:
            return "conservative"
        elif score < 60:
            return "moderate"
        return "aggressive"

    def _constraints(self, category):
        if category == "conservative":
            return {"max_equity": 0.40, "min_bonds": 0.40, "min_cash": 0.10}
        if category == "moderate":
            return {"max_equity": 0.70, "min_bonds": 0.20, "min_cash": 0.05}
        return {"max_equity": 0.90, "min_bonds": 0.05, "min_cash": 0.00}

    def build_profile(self, answers):
        risk_score = self._score_risk(answers)
        category = self._risk_category(risk_score)
        constraints = self._constraints(category)

        return {
            "risk_score": risk_score,
            "risk_category": category,
            "investment_horizon_years": answers["horizon"],
            "goals": answers["goal"],
            "liquidity_need": answers["liquidity_need"],
            "experience_level": answers["experience"],
            "loss_aversion_score": 100 - risk_score,
            "constraints": constraints
        }
