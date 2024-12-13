import csv
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Function to parse dates and prices from the CSV file
def parse_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    date_ranges = rows[0]  # First row contains date ranges
    prices = list(map(float, rows[1]))  # Second row contains prices

    start_dates = []
    valid_prices = []
    
    for date_range, price in zip(date_ranges, prices):
        try:
            # Replace the third "-" in each date range to separate start and end dates
            date_parts = date_range.split('-')
            start_date_str = "-".join(date_parts[:3])  # Take the first three parts as the start date
            start_date = datetime.strptime(start_date_str, "%m-%d-%Y")
            start_dates.append(start_date)
            valid_prices.append(price)
        except ValueError as e:
            print(f"Error parsing date: {date_range}, skipping. Error: {e}")

    return start_dates, valid_prices

# Function to train the model and make predictions
def train_and_predict(start_dates, prices, date_to_predict):
    if not start_dates:
        print("No valid start dates to process.")
        return
    
    # Convert dates to ordinal format
    X = np.array([date.toordinal() for date in start_dates]).reshape(-1, 1)
    y = np.array(prices)
    
    # Train the Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Predict for a new date
    #date_to_predict = input("Enter a future date (MM-DD-YYYY): ")
    try:
        future_date = datetime.strptime(date_to_predict, "%m-%d-%Y")
        future_ordinal = np.array([[future_date.toordinal()]])
        predicted_price = model.predict(future_ordinal)
        print(f"Predicted price for {date_to_predict}: {predicted_price[0]}")
        return predicted_price[0]  # Return the prediction
    except ValueError as e:
        print(f"Error parsing future date: {date_to_predict}. Error: {e}")
        return None

# Main function to combine parsing and ML
def main(date_to_predict):
    file_path = './data_flights.csv'  # Replace with your CSV file path
    start_dates, prices = parse_csv(file_path)
    return train_and_predict(start_dates, prices, date_to_predict)

