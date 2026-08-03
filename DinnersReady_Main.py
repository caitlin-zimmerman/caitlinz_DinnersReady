import pandas as pd
import streamlit as st

## Import utilities from custom modules
from utils.inventory import load_inventory, save_inventory
from utils.api import search_recipes_by_ingredient, search_recipes_by_title, get_recipe_instructions

## Page title and icon
st.set_page_config(page_title="DinnersReady", page_icon=":shallow_pan_of_food:", layout="wide")

## Load custom CSS for sidebar styling
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

## Pull the current inventory 
inventory_df = load_inventory()

## Initialize session state for selected ingredients
if 'selected_ingredients' not in st.session_state:
    st.session_state.selected_ingredients = []

if 'search_results' not in st.session_state:
    st.session_state.search_results = None

## Inventory table and sidebar
with st.sidebar:
    st.header("Your Ingredients")
    st.write("Add or remove ingredients to keep track of what you have on hand.")

    ## Simple 'Add Item' at top of table
    col1, col2 = st.columns([2.5, 1])
    new_item = col1.text_input("Ingredient", placeholder="e.g. zucchini", label_visibility="collapsed", key="add_item_name")
    new_quantity = col2.number_input("Quantity", min_value=1, value=1, step=1, label_visibility="collapsed", key="add_item_quantity")
    
    if st.button("+ Add Ingredient", width='stretch', type="primary"):
        if new_item.strip(): 
            clean_item_name = new_item.strip().lower()

            ## Check if already exists in inventory
            if not inventory_df.empty and clean_item_name in inventory_df['ingredient'].values:
                ## Update quantity
                inventory_df.loc[inventory_df['ingredient'] == clean_item_name, 'quantity'] += new_quantity
            else: 
                ## Add as new row
                new_row = pd.DataFrame([{"ingredient": clean_item_name, "quantity": new_quantity}])
                inventory_df = pd.concat([inventory_df, new_row], ignore_index=True)

            save_inventory(inventory_df)
            st.toast(f"Added {clean_item_name} to pantry!")
            st.rerun()

    st.divider()

    ## Display current inventory count and make edits
    if inventory_df.empty:
        st.info("Your inventory is empty. Please add ingredients.")
    else: 
        for idx, row in inventory_df.iterrows():
            with st.container(border=True): 
                c_name, c_minus, c_quantity, c_plus = st.columns([4, 1, 1, 1], vertical_alignment="center")

                ## Ingredient name - clickable to add to search list
                ingredient_name = row['ingredient'].lower()
                if c_name.button(row['ingredient'].title(), key=f"select_{idx}", 
                                help="Click to add to recipe search", width='stretch'):
                    if ingredient_name not in st.session_state.selected_ingredients:
                        st.session_state.selected_ingredients.append(ingredient_name)
                        st.rerun()

                ## Subtract quantity
                if c_minus.button("-", key=f"dec_{idx}", help="Decrease or delete item"):
                    inventory_df.at[idx, 'quantity'] -= 1
                    ## Delete item if quantity is 0
                    if inventory_df.at[idx, 'quantity'] <= 0:
                        inventory_df = inventory_df.drop(idx)
                    save_inventory(inventory_df)
                    st.rerun()

                ## Quantity number 
                c_quantity.markdown(f"<p style='text-align: center; margin: 0; font-size: 13px; font-weight: bold;'>{row['quantity']}</p>", unsafe_allow_html=True)

                ## Add quantity
                if c_plus.button("+", key=f"inc_{idx}", help="Increase item quantity"):
                    inventory_df.at[idx, 'quantity'] += 1
                    save_inventory(inventory_df)
                    st.rerun()

## Main display area for recipe search
st.header("What's for Dinner Tonight?")
st.divider()
st.subheader("Search for recipes based on your available ingredients, or by recipe name.")

## Search form for mulitple search options
search_type = st.radio("Search by:", options=["Ingredients", "Recipe Name"], horizontal=True)
if search_type == "Ingredients":
    placeholder_text = "e.g., chicken, onion, garlic"  
else: 
    placeholder_text = "e.g., curry, stew, pie"

with st.form("recipe_search_form"):
    ## Pre-populate with selected ingredients from sidebar
    default_value = ", ".join(st.session_state.selected_ingredients) if st.session_state.selected_ingredients else ""
    search_input = st.text_input("Enter search terms:", value=default_value, placeholder=placeholder_text)
    submitted = st.form_submit_button("Search Recipes", type="primary")

## Search button
if submitted: 
    meals = None
    ## Clear selected ingredients after submitting search
    st.session_state.selected_ingredients = []
    
    ## Search by ingredients option
    if search_type == "Ingredients": 
        search_targets = [item.strip() for item in search_input.split(",") if item.strip()]
        
        ## Grab top 3 ingredients from inventory if no input is provided
        if not search_targets: 
            if not inventory_df.empty: 
                all_items = inventory_df['ingredient'].tolist()
                search_targets = all_items[:3] if len(all_items) > 3 else all_items

        if search_targets: 
            with st.spinner(f"Searching recpies with ingredients: '{', '.join(search_targets)}'..."):
                st.session_state.search_results = search_recipes_by_ingredient(search_targets)

        else: 
            st.error("Enter ingredients or add ingredients to your inventory.")
            st.session_state.search_results = None

    ## Search by terms in recipe title
    else: 
        if search_input.strip(): 
            with st.spinner(f"Searching recipe titles containing '{search_input.strip()}'..."):
                st.session_state.search_results = search_recipes_by_title(search_input)
        else: 
            st.error("Type a recipe name or keyword to search.")
            st.session_state.search_results = None

## Display results across reruns
if st.session_state.search_results is not None:
    meals = st.session_state.search_results
    if meals: 
        st.success(f"Found {len(meals)} recipes!")
            
        ## Display recipe cards
        for meal in meals: 
            ## Acordian box to open recipe details
            with st.expander(f"Click to view: {meal['strMeal']}"):
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
                            st.image(details["strMealThumb"], width='stretch')

                else: 
                    st.error("Could not retrieve recipe details. Please try again later.")
    else: 
        st.warning("No recipes found. Try simplifying your search terms.")
           