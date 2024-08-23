import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os


SHEETY_USER = os.environ["SHEETY_USER"]
SHEETY_PASS = os.environ["SHEETY_PASS"]

GENDER = "male"
WEIGHT_KG = 75
HEIGHT_CM = 186
AGE = 28

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]

basic = HTTPBasicAuth(SHEETY_USER, SHEETY_PASS)

today = datetime.now().strftime("%d%m%Y")
now_time = datetime.now().strftime("%X")

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=EXERCISE_ENDPOINT, json=parameters, headers=headers)
result = response.json()

for exercise in result["exercises"]:
    sheet_inputs = {
        "workouts": {
            "date": today,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }

    }

    sheet_response = requests.post(SHEETY_ENDPOINT, json=sheet_inputs, auth=basic)
    print(sheet_response.text)