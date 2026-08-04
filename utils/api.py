import requests
import streamlit as st
from keys import MEALDB_API_KEY

API_KEY = str(MEALDB_API_KEY).strip()
BASE_URL = f"https://www.themealdb.com/api/json/v2/{API_KEY}"

## MealDB API Integration
@st.cache_data(ttl=3600, show_spinner=False)
def search_recipes_by_ingredient(ingredients_list): 
    ## Clean input for API query
    cleaned_ingredients = [i.strip().lower() for i in ingredients_list if i.strip()]

    if not cleaned_ingredients: 
        return []

    ## Join multiple ingredients with commas 
    ingredients_query = ",".join(cleaned_ingredients)

    ## Premium API key (multi-ingredient search)
    url = f"{BASE_URL}/filter.php"
    params = {"i": ingredients_query}
    
    try: 
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            meals = data.get("meals")

            ## If no meals found for multiple ingredients, try searching with the first ingredient only
            if meals is None and len(cleaned_ingredients) > 1:
                params_fallback = {"i": cleaned_ingredients[0]}
                response_fallback = requests.get(url, params=params_fallback)
                if response_fallback.status_code == 200:
                    return response_fallback.json().get("meals") or []

            return meals or []
        return []
    except Exception as e:
        print(f"Network Error: {e}")
        return []                

@st.cache_data(ttl=3600, show_spinner=False)    
def search_recipes_by_title(recipe_title):
    ## Search recipes by words in title
    url = f"{BASE_URL}/search.php"
    params = {"s": recipe_title.strip()}
    try: 
        response = requests.get(url, params=params)
        if response.status_code == 200: 
            data = response.json()
            return data.get("meals") or []
        return []
    except Exception as e: 
        print(f"Network Error: {e}")
        return []

@st.cache_data(ttl=3600, show_spinner=False)    
def get_recipe_instructions(meal_id):
    ## Get recipe instructions by meal ID
    url = f"{BASE_URL}/lookup.php"
    params = {"i": meal_id} 
    try: 
        response = requests.get(url, params=params)
        if response.status_code == 200: 
            data = response.json()
            if data.get("meals"): 
                return data["meals"][0]
    except Exception as e: 
        print(f"Network Error: {e}")
        return None