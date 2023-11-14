#==============================================

# Python code to create APIs returning JSON objects
# for queries sent to a SQLite database

#==============================================




# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



#################################################
# Database exploration
#################################################

# Find the time range in data set (to run the query only once).
date_range=session.query(Measurement.date)

# Find the latest date in the data set.
latest_date=date_range.order_by(Measurement.date.desc()).first()
latest_date=str(latest_date[0])

# Find the first date in the data set (to later provide meaniful messages to run the API).
first_date=date_range.order_by(Measurement.date).first()
first_date=str(first_date[0])

# Calculate the date one year from the last date in data set.
start_date_365=dt.datetime.strptime(latest_date,'%Y-%m-%d').date() - dt.timedelta(days=365)

# Identify the most active station in the dataset (to run the query only once).
active_station=session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc())

session.close()


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

    html="""
    <style>
        .add-link::after {
            content: " " attr(href) "";
        }

    </style>
    
    <body>
    <br>
    <h1> Honolulu, Hawaii Weather Data </h1>
    <br>
    <h2> API documentation </h2>
    <p> To access the API giving the precipitation data for the last 365 days on record from all stations: </p>
    <ul>
    <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
    </ul>
    <br>

    <p> To access the API giving the precipitation data for the last 365 days on record from only the most active station: </p>
    <ul>
    <a href="/api/v1.0/precipitation2">/api/v1.0/precipitation2</a>
    </ul>
    <br>

    <p> To access the API giving the list of the existing monitoring stations: </p>
    <ul>
    <a href="/api/v1.0/stations">/api/v1.0/stations </a>
    </ul>
    <br>

    <p> To access the API giving the list of the monitoring stations having reported weather measurements: </p>
    <ul>
    <a href="/api/v1.0/stations2">/api/v1.0/stations2 </a>
    </ul>
    <br>

    <p> To access the API giving the temperatures from the most active station for the last 365 days on record" </p>
    <ul>
    <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
    </ul>
    <br>

    <p> To access the API giving the Min, Average, and Max temperatures of all the stations since a user-defined start date (yyyy-mm-dd): </p>
    <ul>
    <a class ="add-link" href="/api/v1.0/<start>"> </a>
    </ul>
    <br>

    <p> To access the API giving the Min, Average, and Max temperatures of all the stations between two user-defined dates (yyyy-mm-dd): </p>
    <ul>
    <a class ="add-link" href="/api/v1.0/<start>/<end>"> </a>
    <br>
    </ul>




    </body>
    """
    return (html)
# To display the <start> and <end> in the API link: https://stackoverflow.com/questions/10634494/how-can-i-display-the-href-as-the-text-too

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data for the last 12 months of data on record from all stations"""

    # Query the precipitation
    # Perform a query to retrieve the data and precipitation scores for the last 365 days on record
    prcp_last_12=session.query(Measurement.station, Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date_365).all()

    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    all_precipitation = {}
    for station, date, prcp in prcp_last_12:
        if station not in all_precipitation:
            all_precipitation[station] = {}
        all_precipitation[station][date] = prcp

    return jsonify(all_precipitation)






@app.route("/api/v1.0/precipitation2")
def precipitation2():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data for the last 12 months of data from the most active station"""

    # Query the precipitation
    # Perform a query to retrieve the data and precipitation scores for the last 365 days on record collected by the most active station
    prcp_last_12=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date_365).filter(Measurement.station == active_station[0][0]).all()

    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value.

    all_precipitation = {}
    for date, prcp in prcp_last_12:
        if date not in all_precipitation:
            all_precipitation[date] = {}
        all_precipitation[date] = prcp

    return jsonify(all_precipitation)




@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the station from the station table"""
    # Query the station names
    results=session.query(Station.station,Station.name).all()
  
    session.close()

    all_stations = {}
    for station, name in results:
        if station not in all_stations:
            all_stations[station] = {}
        all_stations[station] = name


    return jsonify(all_stations)




@app.route("/api/v1.0/stations2")
def stations2():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the station and their name from the measurement and the station tables"""

    # Query the station names
    results=session.query(Measurement.station, Station.name).filter(Measurement.station==Station.station).group_by(Measurement.station).all()
  
    session.close()

    # Create a dictionary from the row data
    all_stations = {}
    for station, name in results:
        if station not in all_stations:
            all_stations[station] = {}
        all_stations[station] = name

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the temperature observations of the most active station for the last 365 days on record"""

    # Query the temperature data for the last 365 days on record collected by the most active station
    results=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= start_date_365).filter(Measurement.station==active_station[0][0]).all()
  
    session.close()

    most_active_station = {}  
    for date, tobs in results:
        if date not in most_active_station:
            most_active_station[date] = {}
        most_active_station[date] = tobs 

    return jsonify(most_active_station)




@app.route("/api/v1.0/<start>")
def temp_start_stats(start):
    
    if start=="<start>":
        return jsonify({"Input needed":f"Replace <start> in the URL with a date from {first_date} following the yyy-mm-dd format"})
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the temperature statistics from all stations since a start date"""

    # Query the temperature statistics
    tmin=func.min(Measurement.tobs)
    tavg=func.avg(Measurement.tobs)
    tmax=func.max(Measurement.tobs)
    results=session.query(tmin,tavg,tmax).filter(Measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data
    temp_stats = {}  
    for tmin,tavg,tmax in results:
        if 'TMIN' not in temp_stats:
            temp_stats['TMIN'] = {}
        temp_stats['TMIN'] = tmin 
        if 'TAVG' not in temp_stats:
            temp_stats['TAVG'] = {}
        temp_stats['TAVG'] = tavg 
        if 'TMAX' not in temp_stats:
            temp_stats['TMAX'] = {}
        temp_stats['TMAX'] = tmax 

    return jsonify(temp_stats)




@app.route("/api/v1.0/<start>/<end>")
def temp_start_end_stats(start,end):

    if (start=="<start>" or end=="<end>"):
        return jsonify({"Input needed":f"Replace <start> and <end> in the URL with dates between {first_date} and {latest_date} following the yyy-mm-dd format"})
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the temperature observations between a start date and a end date"""

    # Query the temperature statistics
    tmin=func.min(Measurement.tobs)
    tavg=func.avg(Measurement.tobs)
    tmax=func.max(Measurement.tobs)
    results=session.query(tmin,tavg,tmax).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
  
    session.close()

    # Create a dictionary from the row data and append to a list of stats per station
    temp_stats = {}  
    for tmin,tavg,tmax in results:
        if 'TMIN' not in temp_stats:
            temp_stats['TMIN'] = {}
        temp_stats['TMIN'] = tmin 
        if 'TAVG' not in temp_stats:
            temp_stats['TAVG'] = {}
        temp_stats['TAVG'] = tavg 
        if 'TMAX' not in temp_stats:
            temp_stats['TMAX'] = {}
        temp_stats['TMAX'] = tmax 

    return jsonify(temp_stats)




if __name__ == '__main__':
    app.run(debug=True)




