import streamlit as st
import requests #give python access to the internet

Openweathermap_key = "831bcc60123e44bf868c2ae62826bcd7" #API key from the weather website (openweathermap)
FOURSQUARE_API_key = "ZKZCLUMHW4B0U5P3PZJVIQETLDCIKZT3L2HZF0GPQB2MERPD" #API key from foursquare for activities
UNSPLASH_ACCESS_key = "8wlF9Pb5XZUh_zoCcUS8k9eU-mI_zcwI0rcG_OmGlPM" # API key from Unsplash for destination images


#openweathermap API for weather info

def get_weather(city):
  """Fetch current weather for a city from OpenWeatherMap API"""
  
  response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather", # tell python to get the data from that URL
    params={                                           # settings that we send to the API to tell it exactly what info we want
      "q": city,                                       # q for query (request of info), city not a string because it changes value depending on the user's input
      "appid": Openweathermap_key,                                # inserting the API_key to show that we have permission, appid chosen by openweathermap
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



#Foursquare API for activities per destination

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
        print(response.status_code, response.text)
      
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

# ============================================
# UNSPLASH API FOR DESTINATION IMAGES
# ============================================
# Unsplash is a free photo website with beautiful high-quality travel images
# We use their API to search for photos that match each destination
# To use it, you need a free API key from: https://unsplash.com/developers
# The key below is linked to the SmartTravel account


def get_destination_image(place):
    """
    Fetch a travel photo for a destination from Unsplash

    What this does:
    1. Takes a place name (like "Paris" or "Tokyo")
    2. Searches Unsplash for photos matching "{place} travel landmark"
    3. Returns the URL of the first photo found

    Args:
        place: The name of the destination/city (string)

    Returns:
        A URL string to an image, or None if no image was found
    """
    try:
        # Make a request to Unsplash's search API
        # API endpoint: https://api.unsplash.com/search/photos
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            headers={
                # We need to tell Unsplash who we are with our API key
                # The format is always: "Client-ID YOUR_ACCESS_KEY"
                "Authorization": f"Client-ID {UNSPLASH_ACCESS_key}"
            },
            params={
                # What to search for - we add "travel landmark" to get better results
                # For example: "Paris travel landmark" usually gives nice city photos
                "query": f"{place} travel landmark",
                # We only need 1 photo (the best match)
                "per_page": 1,
                # We want landscape photos (wide format) instead of portrait
                "orientation": "landscape"
            },
            timeout=10  # Give up after 10 seconds if no response
        )

        # Check if the request was successful (status code 200 = OK)
        if response.status_code == 200:
            # Convert the JSON response to a Python dictionary
            data = response.json()

            # Unsplash returns results in a "results" list
            # If the list is not empty, we got at least one photo
            if data["results"]:
                # Return the "regular" size URL of the first result
                # Unsplash provides different sizes: small, regular, full, raw
                # "regular" is good for web display (1080px wide)
                return data["results"][0]["urls"]["regular"]

    except Exception:
        # If anything goes wrong (no internet, API down, etc.), just return None
        # This way the app won't crash - it just won't show an image
        pass

    # Return None if we couldn't find or fetch any image
    return None



