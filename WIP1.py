import requests
api_key = "1" 

ingredient = input("What ingredient is expiring first?")

url = f"https://www.themealdb.com/api/json/v1/{api_key}/filter.php?i={ingredient}"