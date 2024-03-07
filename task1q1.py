import json
import csv
import pandas as pd

# Read the JSON data
# json file was downloaded from https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json using terminal command: % curl https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json > restaurant_data.json
with open('restaurant_data.json', 'r') as file:
    data = json.load(file)

# (For illustration) Print out all the keys - showing all the columns, including those in nested dictionaries and lists.
# def print_columns(data, prefix=''):
#     if isinstance(data, dict):
#         for k, v in data.items():
#             current_prefix = f"{prefix}.{k}" if prefix else k
#             print(current_prefix)
#             print_columns(v, current_prefix)
#     elif isinstance(data, list):
#         for item in data:
#             print_columns(item, prefix)
# print_columns(data)

# Open the CSV file for writing
with open('restaurant_data_cleaned_q1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Define the field names for the selected columns
    selected_fieldnames = [
        'Restaurant Id',
        'Restaurant Name',
        'Country',
        'City',
        'User Rating Votes',
        'User Aggregate Rating',
        'Cuisines'
    ]

    # Create a CSV DictWriter object
    writer = csv.DictWriter(csvfile, fieldnames=selected_fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Loop through each restaurant in all the data entries
    for data_entry in data:
        for restaurant_entry in data_entry['restaurants']:
            restaurant = restaurant_entry['restaurant']
            
            # Prepare the data to write based on selected columns
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
            
            # Write the row to the CSV file
            writer.writerow(row_data)


# Read both restaurant_data_cleaned_q1.csv and Country-Code.xlsx
restaurantdatacleaned = pd.read_csv("restaurant_data_cleaned_q1.csv")
countrycode = pd.read_excel("Country-Code.xlsx", sheet_name='Sheet1')

# Rename Country column from restaurantdatacleaned to prevent column name duplicates
restaurantdatacleaned = restaurantdatacleaned.rename(columns={'Country': 'Country_restaurants'})

# Join Condition
restaurants = restaurantdatacleaned.merge(countrycode, left_on='Country_restaurants', right_on='Country Code', how='left')

# Check if join condition is correct - number of rows in joined table should equal the number of rows in left table
print(f"Shape of left table (restaurant_data_cleaned) is: {restaurantdatacleaned.shape}")
print(f"Shape of joined table (restaurants) is: {restaurants.shape}")

# Cleaning the columns for the desired output
restaurants = restaurants.drop('Country_restaurants', axis=1).drop('Country Code', axis=1)
restaurants = restaurants.reindex(columns=['Restaurant Id', 'Restaurant Name', 'Country', 'City', 'User Rating Votes', 'User Aggregate Rating', 'Cuisines'])

# Export as CSV file
restaurants.to_csv('restaurants.csv', index=False)
