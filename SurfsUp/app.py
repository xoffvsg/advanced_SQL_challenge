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

# Calculate the date one year from the last date in data set.
latest_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
session.close()
x=str(latest_date[0])
start_date=dt.datetime.strptime(x,'%Y-%m-%d').date() - dt.timedelta(days=365)


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
    <h1> Hawaii Weather Data </h1>
    <ul>
    <a href="/api/v1.0/precipitation">Precipitation for the last 365 days on record</a>
    <br>
    <a href="/api/v1.0/stations">Monitoring Stations </a>
    <br>
    <a href="/api/v1.0/tobs">Temperature from the most active station for the last 365 days on record</a>
    <br>
    <a href="/api/v1.0/<start>">Min, Average, and Max temperatures per station since start = yyyy-mm-dd </a>
     <br>
    <a href="/api/v1.0/<start>/<end>">Min, Average, and Max temperatures per station between start = yyyy-mm-dd and end = yyyy-mm-dd</a><br>
    </ul>
    """
    return (html)


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data for the last 12 months of data"""
    # Query the precipitation

    # Perform a query to retrieve the data and precipitation scores for the last 365 days on record
    prcp_last_12=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for date, prcp in prcp_last_12:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)




@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the station from the dataset"""
    # Query the station names
    results=session.query(Station.station,Station.name).all()
  
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station, name in results:
        station_dict = {}
        # station_dict["station"] = station
        station_dict[station] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)




@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the temperature observations of the most active station for the last 365 days on record"""
    # Query the station names
    active_station=session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc())
    results=session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.station==active_station[0][0]).all()
  
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    most_active_station = []
    for station, date, tobs in results:
        station_dict = {}
        # station_dict["station"] = station
        # station_dict["date"] = date
        station_dict[date] = tobs
        most_active_station.append(station_dict)

    return jsonify(most_active_station)




@app.route("/api/v1.0/<start>")
def temp_start_stats(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the temperature observations from a start date"""
    # Query the temperature statistics
    tmin=func.min(Measurement.tobs)
    tavg=func.avg(Measurement.tobs)
    tmax=func.max(Measurement.tobs)
    results=session.query(Measurement.station,tmin,tavg,tmax).group_by(Measurement.station).filter(Measurement.date >= start).all()
  
    session.close()

    # Create a dictionary from the row data and append to a list of stats per station
    temp_stats = []
    for station, tmin,tavg,tmax in results:
        station_dict = {}
        # station_dict["station"] = station
        # station_dict["date"] = date
        station_dict[station] = [tmin,tavg,tmax]
        temp_stats.append(station_dict)

    return jsonify(temp_stats)




@app.route("/api/v1.0/<start>/<end>")
def temp_start_end_stats(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the temperature observations from a start date"""
    # Query the temperature statistics
    tmin=func.min(Measurement.tobs)
    tavg=func.avg(Measurement.tobs)
    tmax=func.max(Measurement.tobs)
    results=session.query(Measurement.station,tmin,tavg,tmax).group_by(Measurement.station).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
  
    session.close()

    # Create a dictionary from the row data and append to a list of stats per station
    temp_stats = []
    for station, tmin,tavg,tmax in results:
        station_dict = {}
        # station_dict["station"] = station
        # station_dict["date"] = date
        station_dict[station] = [tmin,tavg,tmax]
        temp_stats.append(station_dict)

    return jsonify(temp_stats)


if __name__ == '__main__':
    app.run(debug=True)




