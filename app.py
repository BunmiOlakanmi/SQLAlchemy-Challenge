# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

app=Flask(__name__)
@app.route("/")
def homepage():
    return (f"/api/v1.0/precipitation <br>"
    f"/api/v1.0/stations <br>"
    f"/api/v1.0/tobs <br>"
    f"/api/v1.0/<start> <br>"
    f"/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    PrcpQuery = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    precip = []
    for date, prcp in PrcpQuery:
        prcpdict={}
        prcpdict[date]=prcp
        precip.append(prcpdict) 
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    StatQuery = session.query(Station.station).all()
    session.close()
    # stations = []
    # for stat in StatQuery:
    #     # statdict={}
    #     statdict[stat]=station
    #     stations.append(statdict) 
    return jsonify(list(np.ravel(StatQuery)))

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    tobsQuery = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == tobsQuery[0]).all()
    session.close()
    tobsActive = []
    for date, tobs in temps:
        tobsdict={}
        tobsdict[date]=tobs
        tobsActive.append(tobsdict) 
    return jsonify(tobsActive)

@app.route("/api/v1.0/<startDate>")
def start(startDate):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    PrcpQuery = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > startDate).all()
    session.close()
    precip = {}
    for Tmin, Tavg, Tmax in PrcpQuery:
        precip["Tmin"]=Tmin
        precip["Tavg"]=Tavg
        precip["Tmax"]=Tmax
        
    return jsonify(precip)    

@app.route("/api/v1.0/<startDate>/<endDate>")
def StartEnd(startDate, endDate):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    PrcpQuery = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > startDate).filter(Measurement.date < endDate).all()
    session.close()
    precip = {}
    for Tmin, Tavg, Tmax in PrcpQuery:
        precip["Tmin"]=Tmin
        precip["Tavg"]=Tavg
        precip["Tmax"]=Tmax
        
    return jsonify(precip) 

if __name__ == "__main__":
    app.run(debug=True)


