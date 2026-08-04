import os
import pandas as pd
import streamlit as st

INVENTORY_FILE = "data/inventory.csv"

## Load ingredient inventory from CSV file, or creates a new one
@st.cache_data
def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        try: 
            df = pd.read_csv(INVENTORY_FILE)
            if not df.empty and 'ingredient' in df.columns and 'quantity' in df.columns:
                ## Group duplicates together and sum quantities
                df['ingredient'] = df['ingredient'].astype(str).str.strip().str.lower()
                df = df.groupby('ingredient', as_index=False)['quantity'].sum()
                return df
        except Exception as e:
            print(f"Error loading inventory: {e}")

    return pd.DataFrame(columns=["ingredient", "quantity"])

## Save DataFrame to the CSV
def save_inventory(df, file_path=INVENTORY_FILE):
    os.makedirs(os.path.dirname(file_path), exist_ok=True) 
    df.to_csv(file_path, index=False)
    load_inventory.clear()