import requests #give python access to the internet

API_key = "831bcc60123e44bf868c2ae62826bcd7" #API key from the weather website

def get_weather(city):
  """"Get current weather for a city from OpenWeatherMap API"""
  
  response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather", # tell python to get the data from that URL
    params={                                           # settings that we send to the API to tell it exactly what info we want"
      "q": city,                                       # q for query (request of info), city not a string because it changes value depending on the user's input
      "appid": API_key,                                # inserting the API_key to show that we have permission, appid chosen by openweathermap
      "units": "metric"                                # celsius, units chosen by openweathermap, metric as string because it is fixed unlike city
    }                                                  # } closes the dictionary whereas ) closes the function call
  )

  if response.status_code == 200: # API replies with 200 as status code if it worked successfully 
      data = response.json() # convert the data that has come as a response to our request from the API to a dicitionary
      return {
          "temp": data["main"]["temp"], # go into main and then temperature
          "humidity": data["main"]["humidity"],
          "description": data["weather"][0]["description"], #take the first item from the list "weather" and describe
          "wind_speed": data["wind"]["speed"]
      }
  else:
      return None #city not found or API error
