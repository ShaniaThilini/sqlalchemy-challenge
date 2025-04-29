#Import dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

#################################################
# Database Setup
#################################################

# Connect to the database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into ORM classes
Base = automap_base()
Base.prepare(autoload_with=engine)

# Map the tables (use lowercase if needed!)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Get last 12 months
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= year_ago)\
        .all()

    # Create dict {date: prcp}
    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = [s[0] for s in results]
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Find most active station
    most_active = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count().desc()).first()[0]

    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active)\
        .filter(Measurement.date >= year_ago)\
        .all()

    temps = [{date: temp} for date, temp in results]
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def temp_from_start(start):
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs))\
                     .filter(Measurement.date >= start).all()
    
    return jsonify({
        "Start Date": start,
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    })

@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end):
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs))\
                     .filter(Measurement.date >= start)\
                     .filter(Measurement.date <= end).all()
    
    return jsonify({
        "Start Date": start,
        "End Date": end,
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    })

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
