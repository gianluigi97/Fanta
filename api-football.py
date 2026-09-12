import requests
import pandas as pd
import json
from dotenv import load_dotenv
import os

load_dotenv(r"/Users/gianluigimosti/WorkPlace/Fanta/key.env")

api_key = os.getenv("api-football-key")

url = "https://v3.football.api-sports.io/leagues"

payload={}
headers = {
  'x-apisports-key': api_key,
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

