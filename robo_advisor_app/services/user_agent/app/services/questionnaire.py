class QuestionnaireService:

    def __init__(self):
        # Define your questions and scoring rules
        self.questions = {
            "age": {"type": "int"},
            "horizon": {"type": "int"},
            "risk_preference": {"type": "str", "options": ["low", "medium", "high"]},
            "market_reaction": {"type": "str", "options": ["panic", "concerned", "hold", "buy_more"]},
            "experience": {"type": "str", "options": ["beginner", "intermediate", "advanced"]},
            "liquidity_need": {"type": "str", "options": ["low", "medium", "high"]},
            "goal": {"type": "str", "options": ["growth", "income", "preservation"]}
        }

    def get_questionnaire(self):
        return {
            "questions": self.questions,
            "instructions": "Answer all fields to compute your investment profile."
        }

    def validate_answers(self, answers):
        for key, meta in self.questions.items():
            if key not in answers:
                raise ValueError(f"Missing answer for: {key}")

            if meta["type"] == "str" and "options" in meta:
                if answers[key] not in meta["options"]:
                    raise ValueError(f"Invalid value for {key}. Allowed: {meta['options']}")

        return answers
