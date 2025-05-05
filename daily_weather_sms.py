import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv
import schedule
import time

# Step 1: Load environment variables
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")
LOCATION = os.getenv("LOCATION")

# Step 2: Get weather data from WeatherAPI
def get_weather(location):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": location,
        "aqi": "no"
    }
    response = requests.get(url, params=params)
    data = response.json()

    temp = data["current"]["temp_c"]
    desc = data["current"]["condition"]["text"]
    city = data["location"]["name"]
    country = data["location"]["country"]

    return f"Good morning! ☀️\nWeather in {city}, {country}: {desc}, {temp:.1f}°C."

# Step 3: Send SMS using Twilio
def send_sms(body_text):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = client.messages.create(
        body=body_text,
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )
    print(f"✅ SMS sent: {message.sid}")

# Step 4: Combine both steps into one job
def job():
    try:
        weather_text = get_weather(LOCATION)
        send_sms(weather_text)
    except Exception as e:
        print(f"❌ Error: {e}")

# Step 5: Schedule the job every day at 08:00
schedule.every().day.at("08:00").do(job)

print("🕓 Running... Waiting to send weather at 08:00 every day.")

# Optional: Send now for testing remove the "#" and it will send instantly
#job()

# Step 6: Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
