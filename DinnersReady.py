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


## CLI Application Flow

def run_app():
    print("====Welcome to DinnersReady V1====")

    ## Inventory CSV display
    inventory = load_inventory()
    print("\nYour current ingredients: ")
    print(inventory.to_string(index=False))

    ## Get ingredient input from user
    print("\nWhich ingredients would you like to use?")
    user_raw_input = input("Enter ingredient(s) seperated by commas: ")

    ## Break user input into list of ingredients for API query
    search_targets = user_raw_input.split(",")

    ## Call TheMealDB premium API to search recipes by multi-ingredients
    meals = search_recipes(search_targets)

    if meals: 
        print(f"\nWe found {len(meals)} suggested recipes based on your ingredients.")
        print("\nSuggested Recipes: ")

        ## Number and display recipes found
        for idx, meal in enumerate(meals, 1):
            print(f"{idx}. {meal['strMeal']}")

        ## Have user pick recipe based on number
        try: 
            choice = int(input(f"Select a recipe number (1-{len(meals)}) to view steps: "))
            if 1 <= choice <= len(meals): 
                selected_meal = meals[choice -1]
                selected_meal_id = selected_meal['idMeal']

                ## Get instructions
                print(f"\nFetching data for: {selected_meal['strMeal']}...")
                details = get_recipe_instructions(selected_meal_id)

                if details: 
                    print(f"Cooking instructions for: {details['strMeal']}")
                    print(details['strInstructions'])

            else: 
                print("Invalid number selection.")
        except ValueError: 
            print("Enter a valid numbers-only choice.")

    else:
        print("\nNo meals found for those ingredient combinations.")

    ### Manage inventory ###
    ### Need to do use cases of mispellings, nothing submitted, etc. ###
    ### Add intuitive menu navigation ###

if __name__ == "__main__": 
    run_app()
