
from flask import Blueprint, request, jsonify
from database import db
from models import Building, Alert

alert_bp = Blueprint("alert", __name__)


# POST: Create a new alert
@alert_bp.route("/api/alerts", methods=["POST"])
def create_alert():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    building_code = data.get("building_code")
    alert_type = data.get("alert_type")
    message = data.get("message")
    severity = data.get("severity", "Medium")

    if not building_code or not alert_type or not message:
        return jsonify({"error": "Missing required fields"}), 400

    if severity not in ["Low", "Medium", "High", "Critical"]:
        return jsonify({"error": "Invalid severity"}), 400

    building = Building.query.filter_by(
        building_code=building_code
    ).first()

    if not building:
        return jsonify({"error": "Building not found"}), 404

    alert = Alert(
        building_id=building.id,
        alert_type=alert_type,
        message=message,
        severity=severity
    )

    db.session.add(alert)
    db.session.commit()

    return jsonify({
        "message": "Alert created successfully",
        "building_code": building_code,
        "alert_type": alert_type,
        "severity": severity
    }), 201


# GET: Retrieve all alerts
@alert_bp.route("/api/alerts", methods=["GET"])
def get_alerts():

    alerts = Alert.query.order_by(
        Alert.timestamp.desc()
    ).all()

    result = []

    for alert in alerts:

        building = db.session.get(
            Building, alert.building_id
        )

        result.append({
            "id": alert.id,
            "building_code": building.building_code if building else None,
            "alert_type": alert.alert_type,
            "message": alert.message,
            "severity": alert.severity,
            "status": alert.status,
            "timestamp": alert.timestamp.isoformat()
        })

    return jsonify(result), 200
