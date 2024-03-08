# Upon running this python script (python3 task1q1.py), there will be a final output file (restaurants.csv) which contains the extracted data for Task 1 Question 1.
# For the join condition to get Country, the shapes of the left table and joined table are printed in the terminal to check that the join condition is correct (number of rows should be equal).

# Import libraries
import json
import pandas as pd

# Read 'restaurant_data.json'
# restaurant_data.json was downloaded from https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json using terminal command: % curl https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json > restaurant_data.json
with open('restaurant_data.json', 'r') as file:
    data = json.load(file)

# Initialize an empty list to store row data
rows_list = []

# Loop through each restaurant in all the data entries
for data_entry in data:
    for restaurant_entry in data_entry['restaurants']:
        restaurant = restaurant_entry['restaurant']

        # Select required columns and add them to the rows_list
        row_data = {
            'Restaurant Id': restaurant.get('id'),
            'Restaurant Name': restaurant.get('name'),
            'Country': restaurant['location'].get('country_id'),
            'City': restaurant['location'].get('city'),
            'User Rating Votes': restaurant['user_rating'].get('votes'),
            'User Aggregate Rating': restaurant['user_rating'].get('aggregate_rating'),
            'Cuisines': restaurant.get('cuisines')
        }

        # Convert the user aggregate rating to float
        try:
            row_data['User Aggregate Rating'] = float(row_data['User Aggregate Rating'])
        except (ValueError, TypeError):
            row_data['User Aggregate Rating'] = None

        # Add the row to the list
        rows_list.append(row_data)

# Convert rows_list to a DataFrame
restaurant_data_cleaned = pd.DataFrame(rows_list)

# Read 'Country-Code.xlsx'
country_code = pd.read_excel("Country-Code.xlsx", sheet_name='Sheet1')

# Rename Country column from restaurant_data_cleaned to prevent column name duplicates
restaurant_data_cleaned = restaurant_data_cleaned.rename(columns={'Country': 'Country_restaurants'})

# Left Join Condition
restaurants = restaurant_data_cleaned.merge(country_code, left_on='Country_restaurants', right_on='Country Code', how='left')

# Ensure the join condition is correct by comparing shapes (number of rows) of both tables
print(f"Shape of left table (restaurant_data_cleaned) is: {restaurant_data_cleaned.shape}")
print(f"Shape of joined table (restaurants) is: {restaurants.shape}")

# Clean the columns for the desired output
restaurants = restaurants.drop(['Country_restaurants', 'Country Code'], axis=1)
restaurants = restaurants.reindex(columns=['Restaurant Id', 'Restaurant Name', 'Country', 'City', 'User Rating Votes', 'User Aggregate Rating', 'Cuisines'])

# Export as CSV file
restaurants.to_csv('restaurants.csv', index=False)
