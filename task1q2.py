import json
import pandas as pd

# Read 'restaurant_data.json'
with open('restaurant_data.json') as file:
    data = json.load(file)

# Filter for restaurants that have past event in the month of April 2019
filtered_events = []
for restaurant in data:
    if 'restaurants' in restaurant:
        for res in restaurant['restaurants']:
            restaurant_info = res['restaurant']
            if 'zomato_events' in restaurant_info:
                for event in restaurant_info['zomato_events']:
                    event_info = event['event']
                    start_date = event_info['start_date']
                    end_date = event_info['end_date']
                    if '2019-04-01' <= start_date <= '2019-04-30':
                        # Collect all photo URLs and populate empty values (ie. no photos) with "NA"
                        photo_urls = [photo['photo']['url'] for photo in event_info['photos']] if event_info['photos'] else ["NA"]
                        filtered_events.append([
                            event_info['event_id'],
                            restaurant_info['R']['res_id'],
                            restaurant_info['name'],
                            photo_urls,  # Nested list of all photo URLs
                            event_info['title'],
                            start_date,
                            end_date
                        ])

# Convert to pandas dataframe
restaurant_events = pd.DataFrame(filtered_events, columns=['Event Id', 'Restaurant Id', 'Restaurant Name', 'Photo URLs', 'Event Title', 'Event Start Date', 'Event End Date'])

# Convert 'Photo URLs' column to a string to enable CSV export without issues
restaurant_events['Photo URLs'] = restaurant_events['Photo URLs'].apply(lambda urls: '; '.join(urls) if isinstance(urls, list) else urls)

# Export as CSV file
restaurant_events.to_csv('restaurant_events.csv', index=False)
