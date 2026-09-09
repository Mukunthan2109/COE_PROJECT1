import uuid
from app.models import BatchProcurement, db

def calculate_batch_quality_grade(diseased_count, sample_size):
    """
    Calculates defect rate % and assigns batch intake grade:
    - Defect Rate < 5%  -> Grade A (Approved for Premium Processing)
    - Defect Rate 5-15% -> Grade B (Approved for Standard Processing / Sorting)
    - Defect Rate 15-25%-> Grade C (Restricted / Discounted Intake)
    - Defect Rate > 25% -> REJECT (Contaminated / Rejected Intake)
    """
    if sample_size <= 0:
        return 0.0, "Grade A", "Approved"

    defect_rate = (float(diseased_count) / float(sample_size)) * 100.0

    if defect_rate < 5.0:
        grade = "Grade A"
        status = "Approved"
    elif defect_rate <= 15.0:
        grade = "Grade B"
        status = "Conditional (Sorting)"
    elif defect_rate <= 25.0:
        grade = "Grade C"
        status = "Discounted Purchase"
    else:
        grade = "REJECT"
        status = "Rejected Intake"

    return round(defect_rate, 1), grade, status

def create_batch_inspection(crop, supplier_region, total_weight_kg, sample_size_count, diseased_sample_count, notes=None):
    defect_rate, grade, status = calculate_batch_quality_grade(diseased_sample_count, sample_size_count)
    batch_code = f"BATCH-{crop[:3].upper()}-{uuid.uuid4().hex[:6].upper()}"

    batch = BatchProcurement(
        batch_code=batch_code,
        crop=crop,
        supplier_region=supplier_region,
        total_weight_kg=float(total_weight_kg),
        sample_size_count=int(sample_size_count),
        diseased_sample_count=int(diseased_sample_count),
        defect_rate_percent=defect_rate,
        quality_grade=grade,
        intake_status=status,
        inspection_notes=notes
    )

    db.session.add(batch)
    db.session.commit()
    return batch
