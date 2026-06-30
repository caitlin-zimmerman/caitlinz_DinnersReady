import os
import requests
import pandas as pd
from keys import MEALDB_API_KEY

## Track inventory with Pandas

inventory_file = "data/inventory.csv"

## Load ingredient inventory from CSV file, or creates a new one
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

## Inventory management menu function
def manage_inventory_menu(df):
    while True: 
        print("\n==== Inventory Management ====")
        print("1. View Current Inventory")
        print("2. Add or Update Ingredient")
        print("3. Back to main menu")

        choice = input("Select an option (1-3): ").strip()

        if choice == '1': 

            ## Get list of ingredients in inventory
            print("\nYour current ingredients: ")
            print(df.to_string(index=False))

        elif choice == '2': 

            ## Get ingredient name and quantity
            ingredient_name = input("Enter ingredient: ").strip().lower()
            if not ingredient_name: 
                print("Ingredient cannot be empty.")
                continue

            try: 
                quantity = int(input(f"\nEnter quantity for {ingredient_name}: "))
                if quantity <= 0: 
                    print("Enter a quantity greater than 0.")
                    continue
            except ValueError: 
                print("Invalid quantity. Enter only whole numbers.")
                continue

            ## Check if ingredient is on CSV 
            if ingredient_name in df['ingredient'].values:

                ## Update quantity
                df.loc[df['ingredient'] == ingredient_name, 'quantity'] += quantity
                print(f"Updated quantity of {ingredient_name}.")
            else: 
                ## Add ingredient to new row
                new_row = pd.DataFrame([{"ingredient": ingredient_name, "quantity": quantity}])
                df = pd.concat([df, new_row], ignore_index=True)
                print(f"Added {ingredient_name} to inventory.")

            ## Save updated CSV
            save_inventory(df)

        elif choice == '3': 

            ## Back to main menu
            break

        else: 
            print("Invalid choice. Please choose 1, 2, or 3.")

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
    inventory = load_inventory()

    while True: 
        print("\n==== Main Menu ====")
        print("1. Manage Inventory (View or Add Ingredients)")
        print("2. Search Recipes by Ingredients")
        print("3. Exit")

        main_choice = input("Select an option (1-3): ").strip()

        if main_choice == '1': 
            ## Go to inventory management menu / flow
            inventory = manage_inventory_menu(inventory)

        elif main_choice == '2': 
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

        elif main_choice == '3': 
            ## Exit choice
            print("\nThanks for using Dinners Ready! Goodbye.")
            break
        else: 
            print("Invalid choice. Please pick 1, 2, or 3.")

if __name__ == "__main__": 
    run_app()
