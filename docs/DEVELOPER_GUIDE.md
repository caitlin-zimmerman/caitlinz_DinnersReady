# Developer Guide for DinnersReady

This guide is designed for developers maintaining or expanding the DinnersReady project. This guide will cover: 
* High-level overview of project and architecture
* Code execution flow
* Known edge cases
* Future roadmap

---

## Project Overview 
DinnersReady is a Streamlit-based web application using TheMealDB API to help users reduce food waste by finding recipes based on the ingredients they have in their inventory. 

### Implemented and Deferred Specifications

| Feature / Requirement | Status | Implementation Details | 
| --- | --- | --- | 
| Pantry inventory management | Implemented | Continuous CSV storage (`data/inventory.csv`) with add, quantity edit, and delete capabilities. | 
| Multi-ingredient API search | Implemented | Queries the premium TheMealDB API with automatic search fallback to primary ingredients. | 
| Recipe title search | Implemented | Queries TheMealDB API for keyword matches within recipe titles. | 
| Recipe details | Implemented | Fetches the recipe instructions and thumbnail image via the lookup endpoint in TheMealDB API. | 
| Custom styling and layout | Partially Implemented | Light custom CSS applied via `assets/style.css` for sidebar layout. | 
| Expiration date tracking | Deferred | Out of scope. Would require using another API (e.g., Edamam). | 
| Nutritional info / macros | Deferred | Out of scope. Would require using another API (e.g., Edamam). | 

---

## Environment Setup and Deployment

### Python Version and Dependencies
* Python version: Tested and built on Python 3.13
* Core libraries:
  * `streamlit` - Web framework
  * `pandas` - CSV parsing for inventory and data manipulation
  * `requests` - HTTP requests for TheMealDB API

### Package Architecture
```text
CAITLINZ_DINNERSREADY/
├── .streamlit/
│   └── config.toml          # Streamlit theme and server configurations
├── assets/
│   └── style.css            # Custom CSS overrides
├── data/
│   └── inventory.csv        # Local CSV datastore
├── docs/
│   └── DEVELOPER_GUIDE.md   # (This file) Developer documentation
├── utils/
│   ├── __init__.py          # Marks utils as a Python package
│   ├── api.py               # API request functions & st.cache_data decorators
│   └── inventory.py         # Inventory I/O and pandas deduplication
├── DinnersReady_Main.py     # Main application UI and session control
├── keys.py                  # API key file (git-ignored)
├── .gitignore               # Excludes virtual environments and keys
└── README.md                # End-user documentation
```

### Developer Requirements
API Key setup: Make sure keys.py exists in root directory: 
```python
MEALDB_API_KEY = "1" # Replace with premium key if applicable
```

---

## Application Flow

### Architectural data flow: 

```text
[ User action ]
├── [ DinnersReady_Main.py ] 
|   └── [ utils/inventory.py ]          # Pantry management
|        └── [ data/inventory.csv ]  
│   └── [ utils/api.py ]                # API calls
|        └── [ TheMealDB REST API ] 
```

### Step-by-step code execution: 

### 1. App initialization and session state management
* `DinnersReady_Main.py` executes top-down script run on user interaction
* `st.set_page_config()` establishes layout attributes
* `assets/style.css` is custom CSS injected via `st.markdown`
* Session state:
    * `st.session_state.selected_ingredients`: Stores temporary list of ingredients clicked from the sidebar
    * `st.session_state.search_results`: Stores cached API recipe response across reruns

### 2. Inventory operations ( `utils/inventory.py` )
* `load_inventory()`:
    * Reads `data/inventory.csv` into Pandas DataFrame
    * Cleans string whitespace, converts ingredient names to lowercase, aggregates
    * Uses @st.cache_data to minimize read operations
* `save_inventory(df)`:
    * Creates the data/ directory if it doesn't exist, then writes the DataFrame to `data/inventory.csv`
    * Calls `load_inventory.clear()` to invalidate just the inventory cache, so that the next read reflects the update (does not affect the API caches in `utils/api.py`)
 
### 3. Sidebar UI and button logic ( `DinnersReady_Main.py` )
* Renders pantry items using a loop over `inventory_df.iterrows()`
* Every generated widget key uses a unique string combining the action prefix, cleaned ingredient name, and loop index `i`:
    * Ingredient selection button: `key=f"btn_sel_{ing_name}_{i}"`
    * Quantity decrease button: `key=f"btn_dec_{ing_name}_{i}"`
    * Quantity increase button: `key=f"btn_inc_{ing_name}_{i}"`
 
### 4. API integration
API calls are wrapped with `@st.cache_data(ttl=3600)` to optimize load times and reduce request volume
* `search_recipes_by_ingredient(ingredients_list)`:
    * Formats list strings into comma-separated queries
    * Sends GET request to `f"{BASE_URL}/filter.php?i={ingredients_query}"`
    * Fallback logic: if multi-ingredient search returns `None`, it automatically retries with the first ingredient ( `cleaned_ingredients[0]` )
* `search_recipes_by_title(recipe_title)`:
    * Queries `f"{BASE_URL}/search.php?s={recipe_title}"` for keyword matches in recipe titles
* `get_recipe_instructions(meal_id)`:
    * Called for every returned meal on each rerun ( `st.expander` )
    * Queries `f"{BASE_URL}/lookup.php?i={meal_id}"` to retrieve cooking instructions and thumbnail images

---

## Known Issues

### Minor Issues

### 1. TheMealDB multi-ingredient strictness: 
* Issue: The v2 API endpoint performs strict matching across the provided ingredients. If three ingredients are provided and the recipe doesn't contain all three, the API returns `None`.
* Mitigation: A fallback loop in `utils/api.py` searches using the first target ingredient if the multi-search returns empty.

### 2. API calls on rerun: 
* Issue: API calls fire for every recipe result on every rerun, not just expanded cards.

### 3. Error handling: 
* Issue: Network / API failures are indistinguishable in the web app from "No recipes found." 

### Major Limitations

### 1. Local CSV file:
* Issue: User sessions modify the same local `data/inventory.csv` file, therefore it is not appropriate for multi-user access
* Workaround: Replace `utils/inventory.py` with a SQL database

---

## Future Development Roadmap

### 1. Database handling: 
* Transition `data/inventory.csv` to a SQL solution to support multi-user accounts

### 2. Pantry auto-deduction: 
* Add a "Cooked This" button inside the expanded recipe cards that will subtract the used quantities of ingredients from `inventory_df`

### 3. Bulk ingredient upload (grocery receipt)
* Add a way to upload everything you purchased from your online grocery receipt or order

### 4. Add expiration date trackers to ingredients
* Receive alerts to upcoming expiration dates on ingredients in order to prioritize what needs to be used first

### 5. Appropriate unit measurements for ingredients
* Add a way to add ingredients and modify their quantities based on applicable units of measurement (e.g., herbs, liquids)



