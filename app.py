from flask import Flask, jsonify, render_template, request
import pymysql
import requests

app = Flask(__name__)

MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoieXVwZW5nbGl1IiwiYSI6ImNtMjF2a2lpNDAwa28ybXEwNzByeHZkdjEifQ.eJuvRXNJcqKUbAFBwu5xJg"
UV_API_KEY = "openuv-h8j7rm8578eb6-io"

db_config = {
    "host": "fit5120.cja0m8k6e2fo.ap-southeast-2.rds.amazonaws.com",
    "user": "fit5120",
    "password": "fit5120ta03",
    "database": "fit5120"
}

@app.route("/")
def home():
    return render_template("index.html", mapbox_token=MAPBOX_ACCESS_TOKEN)

@app.route("/api/uv")
def get_uv():
    lat = request.args.get("lat", "-37.92")
    lng = request.args.get("lng", "145.12")
    url = f"https://api.openuv.io/api/v1/uv?lat={lat}&lng={lng}"
    headers = {"x-access-token": UV_API_KEY}
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

@app.route("/api/mapbox")
def get_mapbox_data():
    location = request.args.get("location", "Melbourne")
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={MAPBOX_ACCESS_TOKEN}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route("/api/cancer_data")
def get_cancer_data():
    state = request.args.get("state")
    table = request.args.get("type")

    if not state or table not in ["cancer_incidence", "cancer_mortality"]:
        return jsonify([])

    query = f"SELECT year, SUM(count) FROM {table} WHERE state = %s GROUP BY year ORDER BY year;"
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(query, (state,))
    result = cursor.fetchall()
    conn.close()
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
