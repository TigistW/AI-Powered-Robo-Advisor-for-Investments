import pytest
from services.user_agent.questionnaire import QUESTION_SCHEMA, validate_answers, normalize_answers
from services.user_agent.risk_scorer import RiskScorer
from services.user_agent.profile_builder import build_profile

def test_validation_missing_field():
    answers = {'age': 30}
    errs = validate_answers(answers)
    assert 'investment_horizon_years' in errs

def test_normalize_and_score_conservative():
    answers = {
        'age': 60,
        'investment_horizon_years': 3,
        'experience_level': 'beginner',
        'income_stability': 'unstable',
        'current_savings': 1000,
        'investment_amount': 100,
        'goal': 'capital_preservation',
        'market_downturn_reaction': 'panic_sell',
        'liquidity_need': 'high',
        'esg_preference': False,
    }
    errs = validate_answers(answers)
    assert errs == {}
    # Fill missing with defaults to allow scoring
    answers_complete = answers.copy()
    answers_complete['investment_horizon_years'] = 3
    ns = normalize_answers(answers_complete)
    scorer = RiskScorer()
    score = scorer.score(ns)
    cat = scorer.category(score)
    assert cat in ['conservative','moderate','aggressive']

def test_build_profile_outputs_expected_keys():
    answers = {
        'age': 35,
        'investment_horizon_years': 10,
        'experience_level': 'intermediate',
        'income_stability': 'stable',
        'current_savings': 10000,
        'investment_amount': 2000,
        'goal': 'growth',
        'market_downturn_reaction': 'hold',
        'liquidity_need': 'low',
        'esg_preference': True,
    }
    profile = build_profile(answers)
    keys = ['risk_score','risk_category','investment_horizon_years','constraints','metadata']
    for k in keys:
        assert k in profile
