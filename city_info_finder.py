import os
import requests
import wikipediaapi
import streamlit as st
from dotenv import load_dotenv
import time
from huggingface_hub import InferenceClient
# -----------------------------
# Load environment
# -----------------------------
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
client = InferenceClient(token=HF_TOKEN)
st.set_page_config(page_title="City Explorer Agent 🌍", page_icon="🌍")
st.title("🌍 City Explorer Agentic AI")
st.caption("Enter a city, and the agent fetches country, capital, temperature, and a fun fact.")

# -----------------------------
# Functions / Tools
# -----------------------------

def geocode_city(city: str) -> dict:
    """
    Returns country name and state/province for a given city.
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    resp = requests.get(url).json()
    
    if "results" not in resp or len(resp["results"]) == 0:
        return {"error": "City not found. Please provide a valid city name."}
    
    best_match = resp["results"][0]
    country = best_match.get("country")
    state = best_match.get("admin1")  # state/province
    return {"country": country, "state": state}

def get_country_capital(country: str) -> str:
    """
    Returns the official capital of a country.
    """
    url = f"https://restcountries.com/v3.1/name/{country}"
    resp = requests.get(url).json()
    if isinstance(resp, list) and "capital" in resp[0]:
        return resp[0]["capital"][0]  # first capital
    return "Unknown"

def get_city_info(city: str) -> dict:
    geocode = geocode_city(city)
    if "error" in geocode:
        return geocode
    
    country = geocode["country"]
    state = geocode["state"]
    capital = get_country_capital(country)
    
    return {
        "city": city,
        "country": country,
        "country_capital": capital,
        "state": state
    }

def hf_query(prompt: str) -> str:

   
    try:
        result = client.text_generation(
            model="google/flan-t5-small", 
            prompt=prompt,
            max_new_tokens=100,
            temperature=0.2
            
        )
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def get_city_info(city: str) -> dict:
    geocode = geocode_city(city)
    if "error" in geocode:
        return geocode
    
    country = geocode["country"]
    state = geocode["state"]
    capital = get_country_capital(country)
    
    return {
        "city": city,
        "country": country,
        "country_capital": capital,
        "state": state
    }

def get_country_and_capital(city: str) -> dict:
    prompt = f"Tell me the country and capital of {city}. "
    result = get_city_info(city)
    country, capital = None, None
   
    country = result['country']
    capital = result['country_capital']
  
    
    return { "country": country, "capital": capital}


def get_temperature(city: str) -> str:
    if not WEATHER_KEY:
        return "No OpenWeather API key."
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric"
    resp = requests.get(url).json()
    if resp.get("cod") != 200:
        return "Temperature not available"
    temp = resp["main"]["temp"]
    return f"{temp}°C"

def get_wikipedia_fact(city: str) -> str:
    wiki = wikipediaapi.Wikipedia("CityExplorer/1.0 ","en")
    page = wiki.page(city)
    if not page.exists():
        return "No Wikipedia page available."
    summary = page.summary.split(". ")[:2]
    return ". ".join(summary)

# -----------------------------
# Streamlit UI
# -----------------------------
city = st.text_input("Enter a city name:")

if st.button("Explore"):
    if not city:
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Fetching info..."):
            country_info = get_country_and_capital(city)
            temp_info = get_temperature(city)
            wiki_info = get_wikipedia_fact(city)
        
        st.success("City Info Found:")
        st.markdown(f"**City:** {city}")
        st.markdown(f"**Country & Capital:** {country_info}")
        st.markdown(f"**Temperature:** {temp_info}")
        st.markdown(f"**Fun Fact (Wikipedia):** {wiki_info}")
