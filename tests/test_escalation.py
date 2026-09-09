import pytest
from datetime import datetime, timedelta
from app.services.escalation import determine_escalation, calculate_time_to_review

def test_high_confidence_escalation_logic():
    # Confidence >= 0.70 threshold -> Initial screening result
    status = determine_escalation(confidence=0.85, is_supported=True, threshold=0.70)
    assert status == 'Initial screening result'

def test_low_confidence_escalation_logic_edge_case():
    """
    Edge Case 2: Image where model confidence is below threshold
    Expected: Automatically escalate to 'Needs expert review'.
    """
    status = determine_escalation(confidence=0.55, is_supported=True, threshold=0.70)
    assert status == 'Needs expert review'

def test_unsupported_category_escalation_logic():
    status = determine_escalation(confidence=0.90, is_supported=False, threshold=0.70)
    assert status == 'Needs expert review'

def test_time_to_review_calculation():
    t_start = datetime(2026, 9, 3, 10, 0, 0)
    t_end = datetime(2026, 9, 3, 10, 15, 30) # 15 min 30 sec = 930 seconds
    
    elapsed_sec = calculate_time_to_review(t_start, t_end)
    assert elapsed_sec == 930.0

def test_user_example_review_duration_29_47_hours():
    # User example: 2026-09-02 04:44 to 2026-09-03 10:12 -> 29.47 hours
    t_start = datetime(2026, 9, 2, 4, 44, 0)
    t_end = datetime(2026, 9, 3, 10, 12, 0)
    
    elapsed_sec = calculate_time_to_review(t_start, t_end)
    assert elapsed_sec == 106080.0 # 29.4667 hours = 106080 seconds
    hours = elapsed_sec / 3600.0
    assert round(hours, 2) == 29.47

