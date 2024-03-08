# This unit test for Task 1 Question 1 checks if the number of rows in the left DataFrame equals to the number of rows in the joined DataFrame.
# Upon running this python script (command: python3 -m unittest task1q1_unittest.py), if "OK" is printed in the terminal, this means that the unit test is successful.

# Import libraries
import unittest
from task1q1 import join_restaurant_and_country
import pandas as pd

class TestDataJoining(unittest.TestCase):
    def test_join_row_count(self):
        # Create a sample restaurant DataFrame
        restaurant_data = {
            'Restaurant Id': [1, 2],
            'Restaurant Name': ['Restaurant A', 'Restaurant B'],
            'Country_restaurants': ['1', '2'],
            'Other Columns': ['Data A', 'Data B']
        }
        restaurant_df = pd.DataFrame(restaurant_data)
        
        # Create a sample country DataFrame
        country_data = {
            'Country Code': ['1', '2', '3'],
            'Country': ['Country 1', 'Country 2', 'Country 3']
        }
        country_df = pd.DataFrame(country_data)
        
        # Perform the join
        joined_df = join_restaurant_and_country(restaurant_df, country_df)
        
        # Assert that the number of rows in the left DataFrame and joined DataFrame are equal
        self.assertEqual(len(restaurant_df), len(joined_df))

if __name__ == '__main__':
    unittest.main()
