import os
import pandas as pd
import streamlit as st

INVENTORY_FILE = "data/inventory.csv"

## Load ingredient inventory from CSV file, or creates a new one
@st.cache_data
def load_inventory(file_path=INVENTORY_FILE): 
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
def save_inventory(df, file_path=INVENTORY_FILE): 
    df.to_csv(file_path, index=False)
    st.cache_data.clear() 