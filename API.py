import streamlit as st
import requests #give python access to the internet

API_key = "831bcc60123e44bf868c2ae62826bcd7" #API key from the weather website
FOURSQUARE_API_key = "fsq3tJKsojVY8gYyK6rnqZ6nMVtqGnG9RHuGVVoyP3n4Gvg=" #API key from foursquare for activities

def get_weather(city):
  """Fetch current weather for a city from OpenWeatherMap API"""
  
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

def get_activities(city, activities, travel_pace, travel_duration=7):
    """Fetch recommended activities from Foursquare based on user preferences"""

    # Map questionnaire answers to Foursquare category IDs
    category_map = {
        "City Tours": "16000",
        "Nature Hikes": "16032",
        "Historical Sites": "16026",
        "Cultural Experiences (Museums, Local Events)": "10027",
        "Food & Drink Experiences (Cooking Classes, Wine Tasting)": "13000",
        "Relaxation (Spas, Beach Days)": "18000",
        "Adventure Activities (Ziplining, Rafting)": "16032",
        "Nightlife (Bars, Clubs)": "10032",
        "Shopping": "17000",
        "Wildlife Encounters": "16034"
    }

    # Map travel pace to number of activities per day
    pace_map = {
        "Relaxed: Take it slow, enjoy each moment": 2,
        "Moderate: Balance of activities and rest": 3,
        "Packed: See and do as much as possible": 5
    }

    # Get how many activities to return based on pace
    per_day = pace_map.get(travel_pace, 3)
    limit = per_day * travel_duration

    # Get category IDs matching user's selected activities
    categories = ",".join([
        category_map.get(a, "16000") for a in activities
    ])

    # Call Foursquare API
    try:
        response = requests.get(
            "https://api.foursquare.com/v3/places/search",
            headers={"Authorization": FOURSQUARE_API_key},
            params={
                "near": city,
                "categories": categories,
                "limit": limit,
                "sort": "RELEVANCE"
            }
        )

        if response.status_code == 200:
            data = response.json()
            results = []
            for place in data["results"]:
                results.append({
                    "name": place["name"],
                    "category": place["categories"][0]["name"] if place["categories"] else "Attraction",
                    "address": place["location"].get("formatted_address", "Address unavailable")
                })
            return results, per_day
        else:
            return None, per_day
    except Exception:
      return None, per_day
