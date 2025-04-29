# SQLAlchemy Climate Analysis & Flask API

This project performs a basic climate analysis using a SQLite database of Hawaii weather data. It includes:

- A Jupyter Notebook (`climate_starter.ipynb`) with data exploration and visualization using SQLAlchemy ORM, Pandas, and Matplotlib.
- A Flask API (`app.py`) with routes that return precipitation, temperature, and station data in JSON format.

There were some errors during the setup, but the project still works for the core functionality. ¯\\_(ツ)_/¯

## API Routes

- `/api/v1.0/precipitation`
- `/api/v1.0/stations`
- `/api/v1.0/tobs`
- `/api/v1.0/<start>`
- `/api/v1.0/<start>/<end>`

---

### Notes
- Data is loaded from `hawaii_measurements.csv` and `hawaii_stations.csv`, or from `hawaii.sqlite` if already created.
- Built using SQLAlchemy Automap and Flask.

