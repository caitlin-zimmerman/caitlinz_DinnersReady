import os
import requests
import pandas as pd
from keys import MEALDB_API_KEY

## Track inventory with Pandas

def load_inventory(file_path="data/inventory.csv"): 

    ## Load ingredient inventory from CSV file, or creates a new one

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
        data = response.json()
        return data.get("meals", None)
    except Exception as e: 
        print(f"Network Error: {e}")
        return None

