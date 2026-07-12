import os
import requests
import pandas as pd
import streamlit as st
from keys import MEALDB_API_KEY

## Page Title and Icon
st.set_page_config(page_title="DinnersReady V2", page_icon=":fork_and_knife:", layout="wide")

## Backend from DinnersReady V1

## Load ingredient inventory from CSV file, or creates a new one
inventory_file = "data/inventory.csv"

def load_inventory(file_path=inventory_file): 

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if os.path.exists(file_path): 
        return pd.read_csv(file_path)
    else: 
        ## Default data example
        default_data = {
            "ingredient": ["chicken breast", "tomato", "garlic", "onion"],
            "quantity": [4, 4, 1, 2]
        }
        df = pd.DataFrame(default_data)
        df.to_csv(file_path, index=False)
        return df

## Save DataFrame to the CSV
def save_inventory(df, file_path=inventory_file): 
    df.to_csv(file_path, index=False)

## MealDB API Integration

def search_recipes(ingredients_list): 

    ## Clean input for API query
    cleaned_ingredients = [i.strip().lower().replace(" ", "_") for i in ingredients_list]
    ingredients_query = ",".join(cleaned_ingredients)

    ## Premium API key (multi-ingredient search)
    url = f"https://www.themealdb.com/api/json/v2/{MEALDB_API_KEY}/filter.php"
    params = {"i": ingredients_query}
    print(f"Searching for recipes with: {cleaned_ingredients}...")

    try: 
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Connection error: {response.status_code}")
            return None
        
        data = response.json()
        return data.get("meals", None)
    
    except Exception as e: 
        print(f"Network Error: {e}")
        return None
    
def get_recipe_instructions(meal_id):

    ## Get recipe instructions by meal ID
    url = f"https://www.themealdb.com/api/json/v2/{MEALDB_API_KEY}/lookup.php"
    params = {"i": meal_id} 

    response = requests.get(url, params=params)
    if response.status_code == 200: 
        data = response.json()
        if data.get("meals"): 
            return data["meals"][0]
    return None

