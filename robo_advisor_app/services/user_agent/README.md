# User Agent Service

This microservice collects user questionnaire inputs and produces a structured investment profile.

## Endpoints

### `GET /user/questions`
Returns the questionnaire schema.

### `POST /user/profile`
Input:
```json
{
  "answers": {
    "age": 23,
    "horizon": 10,
    "risk_preference": "high",
    "market_reaction": "hold",
    "experience": "beginner",
    "liquidity_need": "medium",
    "goal": "growth"
  }
}
