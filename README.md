# advanced_SQL_challenge
<h1>Module 10 Challenge</h1>

<h2>Honolulu Weather</h2>

This exploration of the weather of Honolulu, HI is based on a collection of daily precipitation and temperature measurements collected from nine weather stations between 2010-01-01 and 2017-08-23.
The data is stored in a SQLite databe containing two tables.
<ul>
The <b> seasurement </b> > table has 5 columns: its index, the identifier of the weather station, the date of collection, the precipitation measurement, and the temperature measurement.
There are 19,550 entries for the daily temperatures, but only 18,103 precipitation measurements (i.e. 1,447 missing values). <br>
The <b> station </b> > table has 6 columns: its index, the identifier of the nine weather stations, their full name, their latitudes, their longitudes, and their elevations.
</ul>
<br>
The last 12 months of data (2016-08-23 to 2017-08-23) are decribed in the figure 1.
![Alt text](image.png)
<br>
The corresponding statistics are shown in the table 1
<br>
Precipitation
n	2021
mean	0.177279
std	0.461190
min	0.000000
25%	0.000000
50%	0.020000
75%	0.130000
max	6.700000

<br>
The most active station is the station USC00519281 located in WAIHEE, which reported 2,772 measurements during the 12 months of data considered. The minimum temperature recorded was 54.0F, the maximum 85.0F, and the average temperature was 71.7F. The distribution of the temperature during this period is shown on the histogram figure 2.
<br>
![Alt text](image-3.png)
<br>

The findings above can be reviewed in the <i>climate_starter.ipynb</i> file.
<br>

Next, several APIs are created in the <i> app.py </i> file that reports jsonify lists from queries made to the SQLite database via SQLAlchemy ORM. The API URLs are tested locally by setting a Flask server session on the localhost computer.
<br>
The link <b>/</b> is the home page documenting the available APIs.<br>

The first API <b>/api/v1.0/precipitation</b> reports a list of dictionaries corresponding to the last 12 months of precipitation data with the date as a key and the corresponding precipitation measurement as the value. Note that the question does not specify if this query should be done for all stations or just for the most active station, therefore the pair date/precipitation is reported as nested dictionaries with the station identifier as the key. Doing otherwise would have only reported the date/precipitation collected by the last station in the query. <br>

The second API <b>/api/v1.0/stations</b> reports the list of the stations from the station table in the database.<br>

The third API <b>/api/v1.0/tobs</b> reports the temperature observations collected by the most active station (USC00519281) over the last 12 months in the dataset<br>

The fourth API <b>/api/v1.0/<start></b> and the fifth  <b>/api/v1.0/<start>/<end></b> report the minimum TMIN, the average TAVG, and the max TMAX temperatures measured by all stations for the dates from the start date to the end date, inclusive .<br>


