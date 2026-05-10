import streamlit as st
import requests #give python access to the internet

OpenWeatherMap_key = "831bcc60123e44bf868c2ae62826bcd7" #API key from the weather website (OpenWeatherMap)
OpenTripMap_key = "5ae2e3f221c38a28845f05b68be55a93f0971363cb46027fedab4d83" #API key from OpenTripMap for activities
UNSPLASH_ACCESS_key = "8wlF9Pb5XZUh_zoCcUS8k9eU-mI_zcwI0rcG_OmGlPM" # API key from Unsplash for destination images


#openweathermap API for weather info

def get_weather(city):
  """Fetch current weather for a city from OpenWeatherMap API"""
  
  response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather", # tell python to get the data from that URL
    params={                                           # settings that we send to the API to tell it exactly what info we want
      "q": city,                                       # q for query (request of info), city not a string because it changes value depending on the user's input
      "appid": OpenWeatherMap_key,                                # inserting the API_key to show that we have permission, appid chosen by openweathermap
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



#OpenTripMap API for activities per destination

def get_activities(city, travel_pace):
    """Fetch tourist attractions from OpenTripMap for a given city"""

    # Map travel pace to number of activities per day
    pace_map = {
        "Relaxed: Take it slow, enjoy each moment": 2,
        "Moderate: Balance of activities and rest": 3,
        "Packed: See and do as much as possible": 5
    }
    per_day = pace_map.get(travel_pace, 3)

    OpenTripMap_key = "5ae2e3f221c38a28845f05b68be55a93f0971363cb46027fedab4d83"

    try:
        # Step 1 — get coordinates of the city
        geo = requests.get(
            "https://api.opentripmap.com/0.1/en/places/geoname",
            params={"name": city, "apikey": OpenTripMap_key}
        )
        geo_data = geo.json()
        lat = geo_data["lat"]
        lon = geo_data["lon"]

        # Step 2 — get attractions near those coordinates
        places = requests.get(
            "https://api.opentripmap.com/0.1/en/places/radius",
            params={
                "radius": 5000,       # 5km radius
                "lon": lon,
                "lat": lat,
                "kinds": "interesting_places",
                "limit": per_day * 7, # enough for all days
                "apikey": OpenTripMap_key
            }
        )
        data = places.json()
        results = []
        for place in data["features"]:
            name = place["properties"]["name"]
            if name:  # skip unnamed places
                results.append({
                    "name": name,
                    "category": place["properties"].get("kinds", "Attraction").split(",")[0],
                    "address": city
                })
        return results, per_day

    except Exception as e:
        print(f"OpenTripMap error: {e}")
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



