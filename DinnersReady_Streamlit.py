import os
import requests
import pandas as pd
import streamlit as st
from keys import MEALDB_API_KEY

## Page title, description, and icon
st.set_page_config(page_title="DinnersReady", page_icon=":shallow_pan_of_food:", layout="wide")

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
    try: 
        response = requests.get(url, params=params)
        if response.status_code == 200: 
            data = response.json()
            if data.get("meals"): 
                return data["meals"][0]
    except Exception as e: 
        print(f"Network Error: {e}")
        return None
    
## Pull the current inventory 
inventory_df = load_inventory()

## Inventory table and sidebar
with st.sidebar:
    st.header("Your Ingredient Inventory")
    st.write("Double-click to add or remove ingredients to keep track of what you have on hand.")

    ## Display current inventory count
    if inventory_df.empty:
        st.warning("Your inventory is empty. Please add ingredients.")
        display_df = pd.DataFrame(columns=["Ingredient", "Quantity"])
    else: 
        display_df = inventory_df.rename(columns={"ingredient": "Ingredient", "quantity": "Quantity"})

    ## Add interactivity to table
    edited_df = st.data_editor(display_df, use_container_width=True, hide_index=True, num_rows="dynamic", column_config={
        "ingredient": st.column_config.TextColumn("Ingredient Name", required=True),
        "quantity": st.column_config.NumberColumn("Quantity", min_value=0, default=1, required=True)
    })

    ## Save changes to inventory
    if not edited_df.equals(display_df):
        ## Rename columns back to original for saving
        final_df = edited_df.rename(columns={"Ingredient": "ingredient", "Quantity": "quantity"})

        ## Remove rows with empty ingredient names
        final_df = final_df.dropna(subset=["ingredient"]) 
        ## Remove rows with zero quantity
        final_df = final_df[final_df["quantity"] > 0]

        ## Save and refresh the table
        save_inventory(final_df)
        st.success("Inventory updated successfully!")
        st.rerun()

## Main display area for recipe search
st.header("What's for Dinner Tonight?")
st.subheader("Search for recipes based on your available ingredients.")
st.write("Enter ingredients you have on hand, separated by commas (e.g., chicken, tomato, garlic).")

## Text input for ingredients
search_input = st.text_input("Enter ingredients:", placeholder="e.g., chicken, tomato, garlic")

## Origianl CLI rules for the search input
search_targets = [item.strip() for item in search_input.split(",") if item.strip()]

## Grab top 3 ingredients from inventory if no input is provided
if not search_targets: 
    if not inventory_df.empty: 
        all_items = inventory_df['ingredient'].tolist()
        search_targets = all_items[:3] if len(all_items) > 3 else all_items
    else: 
        search_targets = []

## Search button
if st.button("Search Recipes", type="primary"): 
    if search_targets: 
        st.write(f"Searching recpies with ingredients: '{', '.join(search_targets)}'...")

        meals = search_recipes(search_targets)

        if meals: 
            st.success(f"Found {len(meals)} recipes!")
            
            ## Display recipe cards
            for meal in meals: 
                ## Acordian box to open recipe details
                with st.expander(f"Click to view: {meal['strMeal']}"):
                    st.write("Getting the recipe details...")
                    
                    details = get_recipe_instructions(meal['idMeal'])

                    if details: 
                        ## Layout text on left and image on right
                        col1, col2 = st.columns([3, 1])

                        with col1: 
                            st.markdown(f"### Directions for {details['strMeal']}")
                            ## Clean recipe instructions text
                            recipe_text = str(details.get("strInstructions", "No instructions available."))
                            ## Use markdown to avoid showing Streamlit docs
                            st.markdown(recipe_text)

                        with col2: 
                            if details.get("strMealThumb"): 
                                st.image(details["strMealThumb"], use_container_width=True)

                    else: 
                        st.error("Could not retrieve recipe details. Please try again later.")
            else: 
                st.warning("No recipes found with the provided ingredients. Try simplifying your search terms.")
        else: 
            st.error("Cannot perform search. Your inventory is empty. Please add ingredients to your inventory or enter them manually.")
