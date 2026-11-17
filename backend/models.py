
from database import db
from datetime import datetime


class Building(db.Model):
    __tablename__ = "buildings"

    id = db.Column(db.Integer, primary_key=True)
    building_code = db.Column(db.String(20), unique=True, nullable=False)
    building_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))


class SensorReading(db.Model):
    __tablename__ = "sensor_readings"

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(250))
    severity = db.Column(db.String(20), default="Medium")
    status = db.Column(db.String(30), default="Pending")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    description = db.Column(db.Text)
    reported_by = db.Column(db.String(100))
    status = db.Column(db.String(30), default="Open")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class ResponseTeam(db.Model):
    __tablename__ = "response_teams"

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    assigned_building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"))
    status = db.Column(db.String(30), default="Available")
