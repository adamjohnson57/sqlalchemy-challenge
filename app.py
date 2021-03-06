#Import Programs
from flask import Flask, jsonify
import pandas as pd 
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Setup Engines and Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

station = Base.classes.station
measurement = Base.classes.measurement

session = Session(engine)

#Setup App with Flask
app = Flask(__name__)

#Create the Flask Routes
@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-24<br/>"
        f"/api/v1.0/2016-08-24/2017-08-23")

#Create Session, Query for last year of data, Create Dictionary from list, and Clean results with JSONIFY
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-8-24").all()

    session.close()

    all_prcp = []
    for date, prcp in results:     
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(station.station).order_by(station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(measurement.date, measurement.tobs, measurement.prcp).\
            filter(measurement.date >= "2016-8-23").\
            filter(measurement.station == "USC00519281").\
            order_by(measurement.date).all()

    session.close()

    all_tobs = []
    for prcp, date, tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()

    session.close()

    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["TMIN"] = min
        start_date_tobs_dict["TAVG"] = avg
        start_date_tobs_dict["TMAX"] = max
        start_date_tobs.append(start_date_tobs_dict)

    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start>/<end>")
def one_year(start, end):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()

    one_year_tobs = []
    for min, avg, max in results:
        one_year_tobs_dict = {}
        one_year_tobs_dict["TMIN"] = min
        one_year_tobs_dict["TAVG"] = avg
        one_year_tobs_dict["TMAX"] = max
        one_year_tobs.append(one_year_tobs_dict)

    return jsonify(one_year_tobs)

if __name__ == "__main__":
    app.run(debug=True)
