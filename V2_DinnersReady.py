import streamlit as st
import pandas as pd

# --- 1. SET UP THE VISUAL PAGE LAYOUT ---
st.set_page_config(page_title="DinnersReady", layout="centered")

st.title("🍳 DinnersReady Kitchen Portal")
st.write("Welcome! This app matches ingredients in your fridge to live recipes.")

# --- 2. SHOWING YOUR INVENTORY (SAMPLED FOR STREAMLIT) ---
st.subheader("🛒 Current Pantry Items")

# Create a sample table (just like your CSV loads)
mock_pantry = {
    "Ingredient Name": ["chicken breast", "tomato", "garlic", "onion"],
    "Stock Quantity": [4, 4, 1, 2]
}
df = pd.DataFrame(mock_pantry)

# st.dataframe instantly prints your table visually so users can click and sort columns!
st.dataframe(df, use_container_width=True)

# --- 3. INTERACTIVE SEARCH BAR ---
st.subheader("🔍 Find a Recipe")

# st.text_input creates an actual text entry block on the web screen
user_ingredients = st.text_input("What are you craving? (Separate items with commas):", placeholder="e.g., chicken, tomato")

# st.button draws a real clickable action button
if st.button("Search Cookbook"):
    if user_ingredients:
        st.info(f"Connecting to remote food database to locate meals containing: **{user_ingredients}**...")
        # This is where your API requests.get() function will run!
    else:
        st.warning("Please type at least one ingredient before searching.")