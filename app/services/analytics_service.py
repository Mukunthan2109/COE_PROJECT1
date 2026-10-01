from datetime import datetime, timedelta
from app.models import Observation, ExpertReview, BatchProcurement, OutbreakAlert, db
from app.services.escalation import get_escalation_analytics

REGIONS = ["North Zone", "South Zone", "Central Region", "East District", "West Valley"]
CROPS = ["Tomato", "Potato", "Rice", "Maize", "Chili", "Grape", "Apple"]


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
    Generates structured analytics data strictly from SQLite database queries.
    Guarantees 100% data consistency across main Dashboard and Analytics Page.
    """
    check_and_trigger_outbreak_alerts()
    analytics = get_escalation_analytics()

    total_obs = Observation.query.count()
    ai_screened_count = Observation.query.filter(
        Observation.model_prediction.isnot(None),
        Observation.model_prediction != '',
        Observation.model_prediction != 'unavailable'
    ).count()

    pending_count = Observation.query.filter_by(status='Needs expert review').count()
    reviewed_count = ExpertReview.query.count()
    escalated_count = Observation.query.filter(
        (Observation.status == 'Needs expert review') | (Observation.status == 'Reviewed by expert')
    ).count()
    high_risk_count = Observation.query.filter_by(risk_level='High').count()

    avg_review_time = analytics.get('avg_review_time_formatted', 'N/A')
    if avg_review_time == "Not enough data yet." or reviewed_count == 0:
        avg_review_time = "N/A"

    if total_obs > 0:
        escalation_rate_pct = f"{round((escalated_count / total_obs) * 100, 1)}%"
    else:
        escalation_rate_pct = "N/A"

    all_obs = Observation.query.order_by(Observation.created_at.asc()).all()

    disease_counts = {}
    crop_counts = {}
    stage_counts = {'Seedling': 0, 'Vegetative': 0, 'Flowering': 0, 'Fruiting': 0, 'Harvest': 0}
    risk_counts = {'Low Risk': 0, 'Medium Risk': 0, 'High Risk': 0}
    status_counts = {'Submitted': 0, 'Escalated': 0, 'Expert Validated': 0}
    conf_values = []
    high_conf = 0
    med_conf = 0
    low_conf = 0
    trend_dict = {}

    for obs in all_obs:
        if obs.crop:
            c = "Maize" if obs.crop in ("Corn", "Maize") else obs.crop
            crop_counts[c] = crop_counts.get(c, 0) + 1

        if obs.crop_stage:
            stage_counts[obs.crop_stage] = stage_counts.get(obs.crop_stage, 0) + 1

        pred = obs.model_prediction
        if pred and pred not in ('unavailable', 'Model unavailable', 'Crop-Image Mismatch'):
            clean_pred = pred.split(' ', 1)[1] if ' ' in pred and pred.split(' ', 1)[0] in ('Tomato', 'Potato', 'Rice', 'Maize', 'Corn') else pred
            disease_counts[clean_pred] = disease_counts.get(clean_pred, 0) + 1

        r = obs.risk_level or 'Medium'
        r_key = f"{r} Risk" if "Risk" not in r else r
        risk_counts[r_key] = risk_counts.get(r_key, 0) + 1

        if obs.status == 'Reviewed by expert':
            status_counts['Expert Validated'] += 1
        elif obs.status == 'Needs expert review':
            status_counts['Escalated'] += 1
        else:
            status_counts['Submitted'] += 1

        if obs.confidence is not None and obs.confidence > 0:
            conf_pct = float(obs.confidence) * 100.0 if obs.confidence <= 1.0 else float(obs.confidence)
            conf_values.append(conf_pct)
            if conf_pct >= 80.0:
                high_conf += 1
            elif conf_pct >= 60.0:
                med_conf += 1
            else:
                low_conf += 1

        date_str = obs.created_at.strftime('%b %d') if obs.created_at else 'Unknown'
        trend_dict[date_str] = trend_dict.get(date_str, 0) + 1

    avg_confidence = round(float(sum(conf_values) / len(conf_values)), 1) if conf_values else None

    heatmap_matrix = []
    for region in REGIONS:
        region_count = Observation.query.filter_by(location_region=region).count()
        escalated = Observation.query.filter(
            Observation.location_region == region,
            (Observation.status == 'Needs expert review') | (Observation.status == 'Reviewed by expert')
        ).count()
        r_level = 'High' if escalated >= 3 else ('Medium' if escalated >= 1 else 'Low')
        heatmap_matrix.append({
            'region': region,
            'total_observations': region_count,
            'escalated_cases': escalated,
            'risk_level': r_level
        })

    active_alerts = OutbreakAlert.query.filter_by(status='Active').order_by(OutbreakAlert.created_at.desc()).all()

    return {
        'total_observations': total_obs,
        'ai_screened_count': ai_screened_count,
        'pending_count': pending_count,
        'reviewed_count': reviewed_count,
        'escalated_count': escalated_count,
        'high_risk_count': high_risk_count,
        'avg_review_time': avg_review_time,
        'escalation_rate_pct': escalation_rate_pct,
        'disease_counts': disease_counts,
        'crop_counts': crop_counts,
        'stage_counts': stage_counts,
        'risk_counts': risk_counts,
        'status_counts': status_counts,
        'avg_confidence': avg_confidence,
        'high_conf_count': high_conf,
        'med_conf_count': med_conf,
        'low_conf_count': low_conf,
        'trend_data': trend_dict,
        'heatmap_matrix': heatmap_matrix,
        'active_alerts': [a.to_dict() for a in active_alerts],
        'summary': analytics
    }
