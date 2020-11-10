import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, cast, Date
from datetime import date

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
hawaii_database_path = "../Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{hawaii_database_path}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

#inspector = inspect(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
  
    # Query
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

 # Create a dictionary from the row data and append to a list of all_data
    all_data = []
    for date, prcp in results:
        Measurement_dict = {}
        Measurement_dict["date"] = date
        Measurement_dict["prcp"] = prcp
        all_data.append(Measurement_dict)

    return jsonify(all_data)
   

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query
    result_stations = session.query(Station.station, Station.id, Station.latitude, Station.elevation, Station.name, Station.longitude).all()

    session.close()

    # Convert list of tuples into normal list
    all_names2 = list(np.ravel(result_stations))

    return jsonify(all_names2)

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most active station for the last year of data"""
    results_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_names3 = list(np.ravel(results_tobs))

    return jsonify(all_names3)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start, end=None):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, 
	the average temperature, and the max temperature 
	for a given start or start-end range.
	When given the start only, calculate TMIN, TAVG, and TMAX 
	for all dates greater than and equal to the start date.
	When given the start and the end date, 
	calculate the TMIN, TAVG, and TMAX for dates 
	between the start and end date inclusive."""
    if end:
    
        start_query = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date > start, Measurement.date < end).all()
    else:
        start_query = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date > start).all()
        print(start_query)
    session.close()
    # Convert list of tuples into normal list
    all_names4 = list(np.ravel(start_query))

    return jsonify(all_names4)

if __name__ == '__main__':
    app.run(debug=True)
