# GovTech-CC4

This repository contains all the datasets and python scripts for Internship 2024's take-home assignment.


TASK 1 ------------------------------------------------------------------

Instructions on how to run the python scripts locally:
1. Clone this repository using the web URL (or by downloading the zip folder).
2. Using Visual Studio Code, paste the web URL (or by opening the downloaded zip folder). This will open the files in VSCode.
3. To run the python scripts for Task 1, type the following commands into the terminal in VSCode (Note: python3 and pandas must be installed).

Python scripts to run:
- Question 1: task1q1.py -> command: "python3 task1q1.py"
  - Question 1 contains a unit test python script: task1q1_unittest.py -> command: "python3 -m unittest task1q1_unittest.py"
- Question 2: task1q2.py -> command: "python3 task1q2.py"
- Question 3: task1q3.py -> command: "python3 task1q3.py"


TASK 2 ------------------------------------------------------------------

1. An Architecture Diagram of the infrastructures required to host the API & System Design Diagram that provides logical flow of the carpark availability API
   
![Architecture Diagram](https://github.com/jaslynyee/GovTech-CC4/assets/91607032/5f5687b9-6ffe-4430-a9d1-1847c82b1a46)

Data Flow:
- Process for Managing User Subscriptions and Reservations:
  - Interaction with a static website enables users to view or book a parking lot.
  - The website sends requests to API Gateway #1 for parking lot reservations, which routes these to the appropriate Lambda functions for processing.
  - Lambda Subscription Manager: This function is responsible for handling user subscriptions and updating user-related information within the DynamoDB: User Info Table.
  - Lambda Reservation Processor: This function deals with reservation requests. It communicates with a payment gateway to handle the parking deposit and records the reservation details in the DynamoDB: Reservations Table once the payment is completed.
  - Payment Gateway: This is an integrated external system working with the Lambda Reservation Processor to manage financial transactions. The Lambda function makes an API call to the external Payment Gateway with the necessary payment information for processing. The payment gateway then sends a response back to the Lambda function, indicating whether the payment was successful or if there was an error.
  - Location Gateway: This is an integrated external system working with the Lambda Reservation Processor to manage the user's location or input location. The API Gateway #1 routes the request to the GPS Location Gateway that the device's operating system provides, to obtain the current GPS coordinates or their desired input location.
  
- Workflow for Updating Parking Availability and Sending Notifications:
  - Updates regarding parking availability are sent through a request to API Gateway #2, which is then managed by the Lambda: Status Updater.
  - Lambda Status Updater: This function updates the parking availability status and logs the time of update in the DynamoDB: Garage Status Table.
  - Lambda Reservation Validator: Validates reservations against the DynamoDB: Reservations Table before the parking status is updated in the DynamoDB: Garage Status Table.
  - Changes in the status table set off a DynamoDB Stream, which in turn triggers the Lambda: Notification Sender.
  - Lambda Notification Sender: This function fetches details from the DynamoDB: User Info Table and disseminates notifications from the mobile application.

2. A Database Schema that depicts the tables

![Database Schema](https://github.com/jaslynyee/GovTech-CC4/assets/91607032/747f722b-3830-4eaf-93d8-7a9f1b36805c)

3. An API document that provides the information of the API/s required

API Gateway #1
- Location Search
  - Endpoint: /search-location
  - Method: GET
  - Description: Retrieves a list of available parking locations based on user query.
  - Request Body:
    - location_input: string, user's search term
  - Response: A list of parking locations with details such as name, address, and availability.

- Parking Reservation
  - Endpoint: /reserve-parking
  - Method: POST
  - Description: Allows users to reserve a parking space.
  - Request Body:
    - user_id: string, the ID of the user making the reservation
    - car_park_no: string, the ID of the parking location
    - reservation_datetime: object, containing the start and end times for the reservation
  - Response: Confirmation of the reservation with a reservation ID.
  
- Subscription Management
  - Endpoint: /manage-subscription
  - Method: POST
  - Description: Allows users to subscribe or unsubscribe from parking services.
  - Request Body:
    - user_id: string, the ID of the user
    - is_subscribed: string, "subscribe" or "unsubscribe"
  - Response: Confirmation of subscription status.

API Gateway #2
- Garage Status Update
  - Endpoint: /update-garage-status
  - Method: POST
  - Description: Endpoint for parking lot systems to update the current status of the garage.
  - Request Body:
    - carpark_number: string, the ID of the garage
    - lots_available: string, the current status of available lots in the garage
  - Response: Acknowledgment of status update.

Error Handling
- Errors will be returned in the standard HTTP response format with an appropriate status code and a descriptive message.
