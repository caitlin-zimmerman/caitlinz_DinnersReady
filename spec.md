Project Spec: DinnersReady

Project Description

This app would help households put all of their groceries to use throughout the week by: 
•	Suggesting recipes from available ingredients
•	Track expiration dates 
•	Apply logic for number of servings
•	Display nutritional information
The app will pull in recipes for the ingredients on hand, and will prioritize those ingredients who are nearing their expiration date. As the ingredient list dwindles or new ingredients are added, suggested recipes will change to make sure food is not being wasted.
The user should be able to import their grocery list if shopping online, and eventually take a picture of their grocery receipt and adjust the available ingredients within their DinnersReady account.
V1 (CLI): Using the free tier of TheMealDB API, a user can interact with the app via the terminal to retrieve recipe suggestions and simple recipe instructions based on their ingredient input. 
V2 (GUI): Using what was built in V1, I would then like to use Streamlit for a more user-friendly experience. It has a built-in calendar date picker that I would like to use for food purchase and expiration dates. It would also help me present the ingredient and recipe data in a more digestible way. I would also like to consider using Edamam to retrieve more information on specific ingredients (like general shelf-life), without having to provide that information myself, hard-coded in a dictionary. Edamam has a number of different APIs that could help with this app, but I also am aware that it could easily lead to feature creep. 


Task Vignettes

1.	Recipe suggestion by ingredient(s) input by user
Cindy is very busy with her and her family’s schedule, and planning meals is one thing that she would like to spend less time and energy doing. She knows that she has four chicken breasts in the fridge that need to be cooked or frozen today, and she also has four tomatoes that need to be used in the next day or two before they need to be thrown out. 
Cindy opens DinnersReady, and chooses the option to ‘Suggest recipes by ingredient’. She inputs chicken breast (4) and tomatoes (4) and selects ‘Generate recipes’. She is presented with five simple recipes that feature those specific ingredients, with minimal other ingredients needed to complete the recipes. 
Once selecting a recipe, Cindy is given the simple instructions to make the meal. 
Details and ideas for later: 
•	Split the ingredients into two separate recipes
•	Option to add additional ingredients that are presented in the suggested recipes (Example: a recipe for garlic tomato basil chicken lists all of the ingredients as either on hand or missing,  and a user can click to add basil as one of their items they have on hand already in their kitchen)

2.	CSV grocery list import and recipe expansion
Tom is a planner and likes to submit his grocery order online for his five person household and pick up his grocery order from the store every Monday after work. He would like to import his grocery list into DinnersReady and receive ideas for what meals he can prepare for himself and his family all week. He knows what types of food they like, but would like to try different ways of preparing them. 
Tom would like to modify the ingredients at upload, removing some grocery line items and adding others manually. He would like to be able to select meals to make, and have those ingredients then be removed or reduced from his DinnersReady inventory so that future suggested recipes take into account the new number of ingredients. 
Tom would also like to adjust the serving size on the recipes to reflect how many he would be cooking that recipe for. 
Details and ideas for later: 
•	Take a picture of a grocery receipt and generate / update the inventory in DinnersReady based on ‘reading’ the text from that receipt 

3.	Personal nutritionist for healthy meal planning and expiration dates
Sally is a personal nutritionist who uses DinnersReady to help her clients expand their meal options, while keeping their favorite healthy ingredients included. Being able to export shopping lists for her clients helps them order and plan meals ahead of time. 
Sally would also like to be able to easily access macro nutrition information and have her customers be alerted to expiration dates of the fresh produce they are buying. Recipes can include suggested ingredient additions in order to modify or build upon their initial simple recipes. 
Details and ideas for later: 
•	Plan by day within app: Monday meal 1, meal 2, meal 3, snack 1, snack 2
•	Suggested recipes based on past preferences, and encouraging new ingredient inclusion to add nutritional variety 


Technical Flow

I sketched out a bare bones version 1 of DinnersReady. It starts with user input, stores that information in a list of dictionaries, sends an API request to TheMealDB for information regarding that ingredient or category and a subsequent recipe suggestion. This suggestion would print in terminal to the user. If the user accepts this suggestion, the information stored in our dictionary needs to update and I’d like to store this information in an continuously updating csv file. 
MealDB is a free API with the universal key “1”. They also have a free method: List all Categories, Area, Ingredients. One of the issues I had while I was testing out different search terms was that I typed in “pasta” to search in the ingredients list, and it returned ‘null.’ However, “pasta” is a category, which will display recipes with spaghetti, fettuccine, etc. I would like to loop through both the ingredient list and the category list to pull results from each, not display duplicates, without creating too much lag time. 
I would like to integrate in V2 some of the functionality that Edamam has when it comes to shelf life and ingredient information. I would need help thinking through how and when to make calls to each app within the same workflow, or if I should be thinking about the workflow differently. 



 
