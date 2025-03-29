from flask import Flask,request,jsonify
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)


API_key = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route("/weather",methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error":"City parameter is required"})
    try:
        params ={
            "q":city,
            "appid":API_key,
            "units":"metric"
         }
        response=requests.get(BASE_URL,params=params)
        data=response.json()

        if response.status_code != 200:
            return jsonify({"error":"City not found"}) ,404
        
        weather_info ={
            "city":data["name"],
            "temperature": data["main"]["temp"],
             "description": data["weather"][0]["description"].capitalize()
        }

        return jsonify(weather_info)
    
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True,port=5000)