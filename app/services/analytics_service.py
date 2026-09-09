from datetime import datetime, timedelta
from app.models import Observation, ExpertReview, BatchProcurement, OutbreakAlert, db
from app.services.escalation import get_escalation_analytics

REGIONS = ["North Zone", "South Zone", "Central Region", "East District", "West Valley"]
CROPS = ["Tomato", "Potato", "Chili", "Corn", "Rice", "Wheat", "Apple", "Grape", "Cotton"]

def check_and_trigger_outbreak_alerts(threshold=3):
    """
    Scans observations created in past 48 hours by region & disease.
    Triggers an active OutbreakAlert if cluster count >= threshold.
    """
    cutoff = datetime.utcnow() - timedelta(hours=48)
    recent_obs = Observation.query.filter(Observation.created_at >= cutoff).all()

    clusters = {}
    for obs in recent_obs:
        if obs.model_prediction and "Healthy" not in obs.model_prediction:
            key = (obs.location_region, obs.crop, obs.model_prediction)
            clusters[key] = clusters.get(key, 0) + 1

    alerts_triggered = []
    for (region, crop, disease), count in clusters.items():
        if count >= threshold:
            existing = OutbreakAlert.query.filter_by(
                region=region, crop=crop, disease=disease, status='Active'
            ).first()

            severity = 'Critical' if count >= 5 else ('High' if count >= 3 else 'Medium')
            msg = f"Outbreak Alert: {count} reported incidents of {disease} in {region} within 48 hours! Priority agronomist field dispatch required."

            if existing:
                existing.incident_count = count
                existing.severity = severity
                existing.alert_message = msg
                alerts_triggered.append(existing)
            else:
                new_alert = OutbreakAlert(
                    region=region,
                    crop=crop,
                    disease=disease,
                    incident_count=count,
                    severity=severity,
                    alert_message=msg
                )
                db.session.add(new_alert)
                alerts_triggered.append(new_alert)

    db.session.commit()
    return alerts_triggered

def get_dashboard_analytics_payload():
    """
    Generates structured analytics data for Chart.js and regional outbreak heatmap.
    """
    check_and_trigger_outbreak_alerts()
    analytics = get_escalation_analytics()

    # 1. Regional Heatmap Grid Data
    heatmap_matrix = []
    for region in REGIONS:
        region_count = Observation.query.filter_by(location_region=region).count()
        escalated = Observation.query.filter(
            Observation.location_region == region,
            (Observation.status == 'Needs expert review') | (Observation.status == 'Reviewed by expert')
        ).count()

        # Risk level based on escalated ratio
        risk_level = 'High' if escalated >= 3 else ('Medium' if escalated >= 1 else 'Low')
        heatmap_matrix.append({
            'region': region,
            'total_observations': region_count,
            'escalated_cases': escalated,
            'risk_level': risk_level
        })

    # 2. Disease Category Breakdown for Pie Chart
    obs_all = Observation.query.all()
    disease_counts = {}
    for o in obs_all:
        label = o.model_prediction or "Unclassified"
        disease_counts[label] = disease_counts.get(label, 0) + 1

    # 3. Batch Procurement Quality Breakdown
    batches = BatchProcurement.query.all()
    grade_counts = {'Grade A': 0, 'Grade B': 0, 'Grade C': 0, 'REJECT': 0}
    for b in batches:
        grade_counts[b.quality_grade] = grade_counts.get(b.quality_grade, 0) + 1

    # 4. Active Outbreak Alerts
    active_alerts = OutbreakAlert.query.filter_by(status='Active').order_by(OutbreakAlert.created_at.desc()).all()

    return {
        'summary': analytics,
        'heatmap_matrix': heatmap_matrix,
        'disease_counts': disease_counts,
        'grade_counts': grade_counts,
        'active_alerts': [a.to_dict() for a in active_alerts],
        'total_batches': len(batches)
    }
