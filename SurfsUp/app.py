# Import the dependencies.
pip install flask


from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect an existing database into a new model
Measurement = Base.classes.measurement
Station = Base.classes.station
# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


# 1. Homepage: List all available routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


# 2. Precipitation route: Return the last 12 months of precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query last 12 months of precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
     # Convert results to dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)


# 3. Stations route: Return a JSON list of stations
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    stations_data = session.query(Station.station).all()
    
    # Convert results to a list
    stations_list = [station[0] for station in stations_data]
    
    return jsonify(stations_list)


# 4. TOBS route: Return last 12 months of temperature observations for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    # Query last 12 months of temperature observations for the most active station
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert results to a list
    temperature_list = [{date: tobs} for date, tobs in temperature_data]
    
    return jsonify(temperature_list)


# 5. Start date route: Return TMIN, TAVG, and TMAX for all dates >= start date
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Query TMIN, TAVG, TMAX for all dates >= start
    temperature_stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()
    
    # Create a dictionary for the results
    temp_stats = {
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    }
    
    return jsonify(temp_stats)


# 6. Start and end date route: Return TMIN, TAVG, and TMAX for a range of dates
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Query TMIN, TAVG, TMAX for dates between start and end
    temperature_stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    # Create a dictionary for the results
    temp_stats = {
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    }
    
    return jsonify(temp_stats)



#################################################
# Flask Routes
#################################################
# Run the app
if __name__ == "__main__":
    app.run(debug=True)


python app.py