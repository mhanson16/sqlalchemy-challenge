import numpy as np

import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Path to sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start<br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def percipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results from your precipitation analysis 
    # (i.e. retrieve only the last 12 months of data) to a dictionary 
    # using date as the key and prcp as the value
    
    # From climate_starter code
    
    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)
    one_year_ago

# Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(measurement.date, (measurement.prcp)).filter(measurement.date >= one_year_ago).all()


    session.close()

    # Convert to dictionary
    precipitation_data = []
    for date, prcp in precipitation:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_data.append(precipitation_dict)


    return jsonify(precipitation_data)


# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():

    #redeclare stations variable to avoid unbouded error
    station = Base.classes.station
    # Create our session (link) from Python to the DB
    session = Session(engine)
# Perform a query to retrieve the data about stations
    stations_info = session.query(station.station, station.name, station.latitude, 
                                  station.longitude, station.elevation).all()

    session.close()

# Stations list
    stations_data = []
    for station, name, latitude, longitude, elevation in stations_info:
        stations_list = {}
        stations_list["Elevation"] = elevation
        stations_list["Longitude"] = longitude
        stations_list["Latitude"] = latitude
        stations_list["Name"] = name
        stations_list["Station ID"] = station
        stations_data.append(stations_list)

    return jsonify(stations_data)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)
    one_year_ago

    # Query the dates and temperature observations of the 
    # most-active station for the previous year of data. 
    # USC00519281 is known to be the most active from part 1
    most_active = session.query(measurement.tobs, measurement.date).filter(measurement.station=='USC00519281', 
                                                         measurement.date >= one_year_ago).all()
    
    session.close()

    # Return a JSON list of temperature observations for the previous year.

    most_active_data = []
    for date, temperature in most_active:
        active_temp_list = {}
        active_temp_list[date] = temperature
        most_active_data.append(active_temp_list)

    return jsonify(most_active_data)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of the minimum temperature, 
    # the average temperature, and the maximum temperature for a specified start

    # start date variable declared
    start = dt.date(2010,1,1)

    start_date = session.query(func.min(measurement.tobs), func.max(measurement.tobs), 
                               func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    
    session.close()

    #list to show max, min, and  avg for start date
    start_date_data = []
    for min, max, avg in start_date:
        start_date_list = {}
        start_date_list["Minimum Temperature"] = min
        start_date_list["Maximum Temperature"] = max
        start_date_list["Average Temperature"] = avg
        start_date_data.append(start_date_list)

    return jsonify(start_date_data)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of the minimum temperature, 
    # the average temperature, and the maximum temperature for a specified start

    # start and end date variable declared
    start = dt.date(2010,1,1)
    end = dt.date(2017,8,23)

    date = session.query(func.min(measurement.tobs), func.max(measurement.tobs), 
                               func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date >= end).all()
    
    session.close()

    #list to show max, min, and  avg for start date
    start_end_date_data = []
    for min, max, avg in date:
        start_date_list = {}
        start_date_list["Minimum Temperature"] = min
        start_date_list["Maximum Temperature"] = max
        start_date_list["Average Temperature"] = avg
        start_end_date_data.append(start_date_list)

    return jsonify(start_end_date_data)


if __name__ == "__main__":
    app.run(debug=True)

