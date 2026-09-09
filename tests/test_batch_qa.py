import pytest
from app.services.batch_qa_service import calculate_batch_quality_grade

def test_grade_a_quality_batch():
    # Defect rate 2% (< 5%) -> Grade A Approved
    defect_rate, grade, status = calculate_batch_quality_grade(diseased_count=2, sample_size=100)
    assert defect_rate == 2.0
    assert grade == "Grade A"
    assert status == "Approved"

def test_grade_b_quality_batch():
    # Defect rate 10% (5-15%) -> Grade B Conditional
    defect_rate, grade, status = calculate_batch_quality_grade(diseased_count=10, sample_size=100)
    assert defect_rate == 10.0
    assert grade == "Grade B"
    assert "Conditional" in status

def test_grade_c_quality_batch():
    # Defect rate 20% (15-25%) -> Grade C Discounted
    defect_rate, grade, status = calculate_batch_quality_grade(diseased_count=20, sample_size=100)
    assert defect_rate == 20.0
    assert grade == "Grade C"
    assert "Discounted" in status

def test_reject_quality_batch():
    # Defect rate 30% (> 25%) -> REJECT
    defect_rate, grade, status = calculate_batch_quality_grade(diseased_count=30, sample_size=100)
    assert defect_rate == 30.0
    assert grade == "REJECT"
    assert "Rejected" in status
