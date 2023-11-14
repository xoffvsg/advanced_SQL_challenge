# advanced_SQL_challenge
<h1>Module 10 Challenge</h1>

<h2>Honolulu Weather</h2>

This exploration of the weather of Honolulu, HI is based on daily precipitation and temperature measurements collected from nine weather stations between 2010-01-01 and 2017-08-23.
The data is stored in a SQLite database containing two tables.
<ul>
The <b>measurement</b> table has 5 columns: the row index, the identifier of the weather station, the date of collection, the precipitation measurement, and the temperature measurement.
There are 19,550 entries for the daily temperatures, but only 18,103 precipitation measurements (i.e. 1,447 missing values). <br>
The <b>station</b> table has 6 columns: the row index, the identifier of the nine weather stations, their full name, their latitudes, their longitudes, and their elevations.
</ul>
<br>
The last 12 months of data (2016-08-23 to 2017-08-23) are depicted in figure 1.

<br>![12_month_precipitation_data](https://github.com/xoffvsg/advanced_SQL_challenge/assets/141395221/94e5e1e7-327d-4a59-bc0b-16343e549f75)
<br>Figure 1<br><br>

The corresponding statistics are shown in the table 1
<br><br>

Stats|Precipitation
--- | ---
n	|2021
mean	|0.177
std|	0.461
min	|0.000
25%	|0.000
50%	|0.020
75%	|0.130
max	|6.700

Table 1
<br><br>

The most active station is the station USC00519281 located in WAIHEE, which reported 2,772 measurements during the 12 months of data considered. The minimum temperature recorded was 54.0F, the maximum 85.0F, and the average temperature was 71.7F. The distribution of the temperatures during this period is shown on the histogram figure 2. <br>
<br>
![12_month_temperature_histogram](https://github.com/xoffvsg/advanced_SQL_challenge/assets/141395221/5f2887a9-1081-426f-a133-18f36ce1fc0e)
<br>
Figure 2
<br><br>

The findings above can be reviewed in the <i>SurfsUp/climate_starter.ipynb</i> file.
<br>

Next, several APIs are created in the <i> SurfsUp/app.py </i> file that reports jsonify dictionaries from queries made to the SQLite database via SQLAlchemy ORM. The API URLs are tested locally by setting a Flask server session on the localhost computer.
<br>
The link **/** is the home page documenting the available APIs.<br>

The first API **/api/v1.0/precipitation** reports a list of dictionaries corresponding to the last 12 months of precipitation data with the date as a key and the corresponding precipitation measurement as the value. Note that the question does not specify if this query should be done for all stations or just for the most active station, therefore the pair date/precipitation is reported as nested dictionaries with the station identifier as the key. Doing otherwise would have only reported the date/precipitation collected by the last station in the query. <br>
This extra step is not necessary if the question was supposed to be applied to a single station and the key:value pair (date:prcp) can be reported directly as shown in the second API **/api/v1.0/precipitation2**, which limits the query to the most active station. <br>

The third API **/api/v1.0/stations** reports the list of the stations from the station table in the database.<br>

Remark: None of the questions, as asked, would require to run a query joining the two tables in the database despite what is mentioned in the **Hint** section of the instructions. Therefore, a fourth API **/api/v1.0/stations2** is volunteered to report the list of the stations identifiers from the measurement table and associate them with the station name queried from the station table in the database. Unsurprisingly, it gives the same output as the **/api/v1.0/stations** API.<br>

The fifth API **/api/v1.0/tobs** reports the temperature observations collected by the most active station (USC00519281) over the last 12 months in the dataset<br>

The sixth API **/api/v1.0/start** and the seventh  **/api/v1.0/start/end** report the minimum TMIN, the average TAVG, and the max TMAX temperatures measured by all stations between the selected start and end dates, inclusive .<br>




