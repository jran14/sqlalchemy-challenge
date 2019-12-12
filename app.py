#dependencies 
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import json
from decimal import Decimal
import datetime as dt
from sqlalchemy import and_, func
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Create references to the invoices and invoice_items tables called Invoices and Items
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes


@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )
#homepage
# @app.route("/")
# def homepage():
#   return (
#         f"Available Routes:<br/>"
#         f"/api/v1.0/precipitation<br/>"
#         f"/api/v1.0/stations<br/>"
#         f"/api/v1.0/tobs<br/>"
#         f"/api/v1.0/<start>/<end><br/>")

#####################################################

#query for results from the measurement table
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create a database session object
    session = Session(engine)

    #query dor dates and precp levels
    prcp_query = session.query(Measurement.date, Measurement.prcp).all()

    # Convert to dict
    data_list=[]
    for row in prcp_query:
        data_dict = {'Dates': row[0], 'Precipitation level': str(row[1])}
        data_list.append(data_dict)

    return jsonify(data_list)

##############################################################

#query for results from the stations table
@app.route("/api/v1.0/stations")
def stations():
    
    # Create a database session object
    session = Session(engine)
    
    # Query for the stations 
    results2 = session.query(Station.station).all()

    return jsonify(results2)


#############################################################

#query for the temperatures and dates from the measurement table
@app.route("/api/v1.0/tobs")
def temps():

    # Create a database session object
    session = Session(engine)

    #last date
    last_date = session.query(Measurement.date).\
            order_by(Measurement.date.desc()).first().date

    from_date = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query for data within date range
    results3 = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= from_date).all()
   
    return jsonify(results3)


############################################################

#query for the min temp, avg temp, max temp in the date range
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVG, and TMAX"""

    # Create a database session object
    session = Session(engine)

    results4= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    return jsonify(results4)

if __name__ == '__main__':
    app.run(debug=True)
