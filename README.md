# DinnersReady

**DinnersReady** is a recipe finder built with Python and Streamlit. DinnersReady makes it easy for you to track and modify your grocery inventory, and then use those ingredients to search delicious recipes you can make using **TheMealDB** API. 

---

## Prerequisites

* **Python 3.13**

## Setup and installation

Follow these steps to get DinnersReady running on your local machine: 

### 1. Set up your API key
DinnersReady relies on **TheMealDB** API to fetch recipes. 
  * Create a file named keys.py in the project root folder
  * Add your TheMealDB API key formatted like this:
      * `MEALDB_API_KEY = "1"`
      * replace '1' with your custom premium API key if you have one
      * "1" is the public test key provided by TheMealDB. Multi-ingredient search requires purchasing a premium API key

### 2. Install required dependencies
You can install manually via: 
```python
pip install streamlit pandas requests
```

---

## How to run the app

1. Open your terminal in the project directory. 
2. Launch the Streamlit server by executing: 
```python
python -m streamlit run DinnersReady_Main.py
```
3. Your default web browser will automatically open to http://localhost:8501

---

## User guide
A step-by-step walkthrough

### Step 1: Manage your ingredient inventory
On the left sidebar: 
* Type an ingredient name into the **Ingredient** text box (e.g., zucchini, egg, garlic).
* Set the quantity of that ingredient and click **+ Add Ingredient**.
* Use the + and - buttons next to each pantry item to adjust quantities. Decreasing the quantity to 0 will remove the item.

<img width="292" height="370" alt="image" src="https://github.com/user-attachments/assets/53182abd-c5d9-4e17-b569-1bc18b0e626d" />

### Step 2: Search for recipes
In the main screen display: 
* Select your preferred search method: **Ingredients** or **Recipe Name**
* Type in 1-3 ingredients, separated by commas (*premium API needed for multi-ingredient search)
* Quick fill: Click on any ingredient button in your sidebar inventory list to auto-populate the search box
* Click **Search Recipes**

<img width="461" height="371" alt="image" src="https://github.com/user-attachments/assets/1e27e396-f4b0-4577-8332-cf4a9679fa44" />

### Step 3: View cooking instructions
* Search results will display in expandable card sections
* Click on any recipe title card to reveal the cooking instructions and meal photo

<img width="462" height="636" alt="image" src="https://github.com/user-attachments/assets/10f08ee2-f540-48a8-b864-3b2d3e357c5f" />

---

## Troubleshooting and common errors

| Issue / Error Message | Cause | How to Fix |
| --- | --- | --- |
| `No recipes found` | TheMealDB search requires exact ingredient names or terms. | Try searching single or common ingredients (e.g., `chicken` instead of `chicken thighs`). | 
| `Network Error` | Invalid API URL or missing internet connection. | Make sure keys.py is in the root folder, use public TheMealDB API key = "1", or purchase premium API key. |
| Flashing UI or Unresponsive Buttons | Stale browser cash or leftover Python background process. | Clear Streamlit's cache from your browser and/or restart VSCode/Terminal. | 

---

## Known limitations
* Inconsistent ingredient matching: Multi-ingredient filtering (premium API only) can strictly match recipes containing all search terms, but also include some recipes that don't have an ingredient that was specified. 
* Local CSV: Pantry inventory is stored locally in data/inventory.csv. Clearing or deleting this file resets your inventory.




