
from flask import Blueprint, request, jsonify
from database import db
from models import Building, SensorReading

sensor_bp = Blueprint("sensor", __name__)


# POST: Receive sensor readings
@sensor_bp.route("/api/sensor-readings", methods=["POST"])
def receive_sensor_reading():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    building_code = data.get("building_code")
    sensor_type = data.get("sensor_type")
    value = data.get("value")
    unit = data.get("unit")

    if not building_code or not sensor_type or value is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        value = float(value)
    except (ValueError, TypeError):
        return jsonify({"error": "Value must be numeric"}), 400

    building = Building.query.filter_by(
        building_code=building_code
    ).first()

    if not building:
        return jsonify({"error": "Building not found"}), 404

    reading = SensorReading(
        building_id=building.id,
        sensor_type=sensor_type,
        value=value,
        unit=unit
    )

    db.session.add(reading)
    db.session.commit()

    return jsonify({
        "message": "Sensor reading saved successfully",
        "building_code": building_code,
        "sensor_type": sensor_type,
        "value": value
    }), 201


# GET: Retrieve all sensor readings
@sensor_bp.route("/api/sensor-readings", methods=["GET"])
def get_sensor_readings():

    readings = SensorReading.query.order_by(
        SensorReading.timestamp.desc()
    ).all()

    result = []

    for reading in readings:

        building = db.session.get(
            Building, reading.building_id
        )

        result.append({
            "id": reading.id,
            "building_code": building.building_code if building else None,
            "sensor_type": reading.sensor_type,
            "value": reading.value,
            "unit": reading.unit,
            "timestamp": reading.timestamp.isoformat()
        })

    return jsonify(result), 200
