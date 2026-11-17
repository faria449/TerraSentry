
from flask import Flask, jsonify
from database import db
from routes.sensor_routes import sensor_bp
from routes.alert_routes import alert_bp
import models

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///terra_sentry.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(sensor_bp)
app.register_blueprint(alert_bp)
with app.app_context():
    db.create_all()

    # Add initial buildings if they do not exist
    if not models.Building.query.filter_by(building_code="BD-001").first():
        db.session.add(models.Building(
            building_code="BD-001",
            building_name="Building A",
            location="Monitoring Zone A"
        ))

    if not models.Building.query.filter_by(building_code="BD-002").first():
        db.session.add(models.Building(
            building_code="BD-002",
            building_name="Building B",
            location="Monitoring Zone B"
        ))

    db.session.commit()


@app.route("/")
def home():
    return jsonify({
        "project": "TerraSentry",
        "message": "TerraSentry Backend is Running!",
        "status": "Online"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "Healthy",
        "server": "Flask",
        "database": "Connected"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
