# City Explorer Agent

A simple **agentic AI application** that provides information about cities.  

Given a city name, the app can return:  
- Country  
- Country capital  
- State/province  
- Optional fun facts about the city  

It combines **structured APIs** and **Wikipedia** to provide information in a reliable and interactive way.

---

## Features

- Uses **Open-Meteo Geocoding API** to get city and country information.  
- Uses **REST Countries API** to fetch the country’s capital.  
- Uses **Wikipedia** to fetch fun facts about the city.  
- Provides **clear error messages** for invalid or misspelled city names.  
- Built as a **basic agentic application** (city name → queries → aggregated results).

---

## Tech Stack

- Python 3.9+  
- Streamlit for frontend  
- Requests for API calls  
- Wikipedia API for fun facts  

---

## Usage

1. Clone the repository  
    ```bash
   git clone https://github.com/j-swaminathan/city_explorer.git
   cd city_explorer ```

2. Create and activate a virtual environment:
   ```bash
  python3 -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate      # Windows ```

3. Install requirements:
    ```bash
   pip install -r requirements.txt ```

4. Run the app:
    ```bash 
streamlit run city_info_finder.py ```


Enter a city name and explore its details!


## Notes

- The app only works with valid city names.

- Misspelled names may return an error or incorrect results.

- Fun facts are fetched from Wikipedia and may vary in length and detail.