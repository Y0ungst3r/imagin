from influxdb import InfluxDBClient
import time


db_params = {
    "host": "192.168.1.1",
    "username": "atlas",
    "password": "AtlasItkDataBase",
    "database": "lab",
    "port": 8086,
}
db_client = InfluxDBClient(
    db_params["host"],
    db_params["port"],
    db_params["username"],
    db_params["password"],
    db_params["database"]
)
