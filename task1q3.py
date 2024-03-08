# Upon running this python script (python3 task1q3.py), there will be no final output file,
# but the thresholds for Task 1 Question 3 will be printed in the terminal.

# Import libraries
import json
import pandas as pd

# Read 'restaurant_data.json'
with open('restaurant_data.json', 'r') as file:
    data = json.load(file)

# Select required columns
restaurants_data = []
for item in data:
    for restaurant_entry in item['restaurants']:
        restaurant = restaurant_entry['restaurant']
        user_rating = restaurant['user_rating']
        aggregate_rating = user_rating['aggregate_rating']
        rating_text = user_rating['rating_text']
        # Ensure aggregate_rating is a float and not "0"
        if aggregate_rating and aggregate_rating != "0":
            restaurants_data.append({"aggregate_rating": float(aggregate_rating), "rating_text": rating_text})

# Organize data by rating_text
ratings_data = {}
for restaurant in restaurants_data:
    rating_text = restaurant["rating_text"]
    if rating_text not in ratings_data:
        ratings_data[rating_text] = []
    ratings_data[rating_text].append(restaurant["aggregate_rating"])

# Determine thresholds (min and max) for the different rating text based on aggregate rating
thresholds = {}
for rating_text, ratings in ratings_data.items():
    thresholds[rating_text] = {
        "min": min(ratings),
        "max": max(ratings)
    }

# Convert thresholds dictionary to a DataFrame
thresholds_df = pd.DataFrame.from_dict(thresholds, orient='index')
thresholds_df.reset_index(inplace=True)
thresholds_df.columns = ['Rating Text', 'Minimum', 'Maximum']

# Select the following ratings only
thresholds_df = thresholds_df.loc[thresholds_df['Rating Text'].isin(['Excellent', 'Very Good', 'Good', 'Average', 'Poor'])]

# Reorder the DataFrame
order = ['Excellent', 'Very Good', 'Good', 'Average', 'Poor']
thresholds_df['Rating Text'] = pd.Categorical(thresholds_df['Rating Text'], categories=order, ordered=True)
thresholds_df = thresholds_df.sort_values('Rating Text')

print(thresholds_df)
