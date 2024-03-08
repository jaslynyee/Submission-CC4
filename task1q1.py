import json
import csv
import pandas as pd

# Read 'restaurant_data.json'
# restaurant_data.json was downloaded from https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json using terminal command: % curl https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json > restaurant_data.json
with open('restaurant_data.json', 'r') as file:
    data = json.load(file)

# Create csvfile 'restaurant_data_cleaned_q1.csv' to store the cleaned dataset
with open('restaurant_data_cleaned_q1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Define the column names for the output csvfile
    selected_fieldnames = [
        'Restaurant Id',
        'Restaurant Name',
        'Country',
        'City',
        'User Rating Votes',
        'User Aggregate Rating',
        'Cuisines'
    ]

    # Initializes a DictWriter object to write dictionaries to csvfile using selected_fieldnames as column headers
    writer = csv.DictWriter(csvfile, fieldnames=selected_fieldnames)
    
    # Writes the header row to csvfile based on those field names
    writer.writeheader()
    
    # Loop through each restaurant in all the data entries
    for data_entry in data:
        for restaurant_entry in data_entry['restaurants']:
            restaurant = restaurant_entry['restaurant']
            
            # Select required columns
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

# Left Join Condition
restaurants = restaurantdatacleaned.merge(countrycode, left_on='Country_restaurants', right_on='Country Code', how='left')

# Check if join condition is correct - number of rows in joined table should equal the number of rows in left table
print(f"Shape of left table (restaurant_data_cleaned) is: {restaurantdatacleaned.shape}")
print(f"Shape of joined table (restaurants) is: {restaurants.shape}")

# Cleaning the columns for the desired output
restaurants = restaurants.drop('Country_restaurants', axis=1).drop('Country Code', axis=1)
restaurants = restaurants.reindex(columns=['Restaurant Id', 'Restaurant Name', 'Country', 'City', 'User Rating Votes', 'User Aggregate Rating', 'Cuisines'])

# Export as CSV file
restaurants.to_csv('restaurants.csv', index=False)
