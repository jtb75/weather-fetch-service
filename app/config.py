import os

class Config:
    API_KEY = os.getenv("API_KEY")
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
