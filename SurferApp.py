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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
        f"/api/v1.0/stations>"
        f"/api/v1.0/tobs>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
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



if __name__ == '__main__':
    app.run(debug=True)