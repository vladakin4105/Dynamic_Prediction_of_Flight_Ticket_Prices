from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import multiprocessing
import time
import csv
import re

import pred

# Configure Chromium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def app_data_scrap(buff,times,from_location,to_location,departure_date,return_date):
    
    # Path to Chromium WebDriver (installed as `chromium-chromedriver`)
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

    # Open Chromium, wait 5 seconds, and then close it
    time.sleep(0.2)
    try:
        driver.get("https://www.google.com/travel/flights")
        time.sleep(0.3)
        try:
            accept_button = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH,'//span[@jsname="V67aGc" and text()="Accept all"]'))
            )
            accept_button.click()
            print("Clicked 'Accept all' button.")
        except Exception as e:
            print("No 'Accept all' button found or error clicking it:", e)
        
        print("Chromium opened successfully!")
        
        
        input_field = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//input[@aria-label="Where from?"]'))
        )
        input_field.clear()
        input_field.send_keys(from_location)
        time.sleep(0.5)
        
        try:
            dropdown_options = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//li[@role="option"]'))
            )
            print(f"Found {len(dropdown_options)} dropdown options.")

            # Filter out options with 'None' in their 'aria-label'
            valid_options = [option for option in dropdown_options if option.get_attribute("aria-label")]

            # Log all valid dropdown options
            for idx, option in enumerate(valid_options, start=1):
                print(f"Valid Option {idx}: {option.get_attribute('aria-label')}")

            # Interact with the first valid option
            if valid_options:
                first_valid_option = valid_options[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", first_valid_option)  # Scroll into view
                driver.execute_script("arguments[0].click();", first_valid_option)  # Click using JavaScript
                print("Clicked the first valid dropdown option using JavaScript.")
            else:
                print("No valid dropdown options found.")
        except Exception as e:
            print("Error selecting the first valid dropdown option:", e)
        
        time.sleep(0.3)
        
        input_to = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Where to? "]'))
        )
        input_to.clear()  # Clear any pre-filled text
        input_to.send_keys(to_location)
        time.sleep(0.5)
        
        try:
            dropdown_options = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//li[@role="option"]'))
            )
            print(f"Found {len(dropdown_options)} dropdown options.")

            # Filter out options with 'None' in their 'aria-label'
            valid_options = [option for option in dropdown_options if option.get_attribute("aria-label")]

            # Log all valid dropdown options
            for idx, option in enumerate(valid_options, start=1):
                print(f"Valid Option {idx}: {option.get_attribute('aria-label')}")

            # Interact with the first valid option
            if valid_options:
                first_valid_option = valid_options[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", first_valid_option)  # Scroll into view
                driver.execute_script("arguments[0].click();", first_valid_option)  # Click using JavaScript
                print("Clicked the first valid dropdown option using JavaScript.")
            else:
                print("No valid dropdown options found.")
        except Exception as e:
            print("Error selecting the first valid dropdown option:", e)
        time.sleep(0.4)
        
        try:
            
            input_departure_date = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH,'//input[@aria-label="Departure"]'))
            )
            #driver.find_element(By.XPATH,'//input[@aria-label="Departure"]')
            input_departure_date.clear()
            input_departure_date.send_keys(departure_date)
            time.sleep(0.7)
            input_departure_date.send_keys(Keys.ENTER)
            print(f'Entered "{departure_date}"')
        except Exception as e:
            print("Eroare la introducerea datei de plecare:", e)
        
        time.sleep(0.7)

        try:
            
            input_return_date = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH,'//input[@aria-label="Return"]'))
            )
            #driver.find_element(By.XPATH,'//input[@aria-label="Return"]')
            input_return_date.clear()
            input_return_date.send_keys(return_date)
            time.sleep(1)
            input_return_date.send_keys(Keys.ENTER)
            print(f'Entered "{return_date}"')
        except Exception as e:
            print("Eroare la introducerea datei de întoarcere:", e)
        
        time.sleep(1)
        try:
            search_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@jsname="V67aGc" and text()="Search"]'))
            )
            search_button.click()
            print("Search button found and clicked.")
        except Exception as e:
            print("Error finding or clicking the search button:", e)

        #toate zborurile sunt intr-o lista unde fiecare element are clasa "pIav2d"
        time.sleep(1)  
        
        try:
            filter_flights = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Stops, Not selected"]'))
            )
            filter_flights.click()
            print("clicked for filter")
            time.sleep(0.5)
            try:
                option_filter = WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.XPATH,'//input[@aria-label="Nonstop only"]'))
                )
                option_filter.click()
                print("option selected")
            except Exception as e:
                print("Error picking option for filter")
        except Exception as e:
            print("Error clicking for filter")

        time.sleep(0.5)
        try:
            list_more = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//button[@aria-label="View more flights"]'))
            )
            list_more.click()
            print("clicked for more flights")
        except Exception as e:
            print("Error clicking search for more")
        
        
        time.sleep(4)
        
        flight_elements = WebDriverWait(driver,20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "pIav2d"))
        )
        #driver.find_elements(By.CLASS_NAME, "pIav2d")
        
        prices = []
        if len(flight_elements) > 0:
            for flight in flight_elements:
                if flight:
                    if flight.text:
                        flight_text = flight.text
                        match = re.search(r'RON\s([\d,]+)', flight_text)  # Match 'RON' followed by a number
                        if match:
                            price = match.group(1).replace(',', '')  # Remove commas for numeric processing
                            prices.append(int(price))  # Convert price to integer for later use
            if len(prices) != 0:
                times.append(f"{departure_date}-{return_date}")
                buff.append(sum(prices)/len(prices))
    finally:
        driver.quit()
        print("Chromium closed.")
        time.sleep(0.3)


def main(from_location, to_location, pred_date, progress_callback,solution_update):
    departure_date = datetime.now() + timedelta(days=1)
    return_date = datetime.now() + timedelta(days=7)
    max_weeks = 40

    # Define shared structures to collect results
    manager = multiprocessing.Manager()
    price_data = manager.list()
    time_data = manager.list()
    
    def app_data_scrap_wrapper(price_list, time_list, dep, ret, from_loc, to_loc):
        # This function acts as a wrapper for app_data_scrap to collect data into shared lists
        app_data_scrap(price_list, time_list, from_loc, to_loc, dep, ret)

    # Initialize and manage processes
    processes = []
    for week in range(max_weeks):
        formatted_departure_date = departure_date.strftime("%m-%d-%Y")
        formatted_return_date = return_date.strftime("%m-%d-%Y")
        
        p = multiprocessing.Process(
            target=app_data_scrap_wrapper,
            args=(price_data, time_data, formatted_departure_date, formatted_return_date, from_location, to_location)
        )
        processes.append(p)
        p.start()
        
        # Ensure no more than 3 processes run simultaneously
        if len(processes) >= 3:
            for p in processes:
                p.join()  # Wait for processes to finish
            processes = []  # Clear the list of completed processes

        # Update dates for the next iteration
        departure_date += timedelta(weeks=1)
        return_date += timedelta(weeks=1)

        # Report progress
        progress = int(((week + 1) / max_weeks) * 100)
        progress_callback(progress)
    
    # Wait for any remaining processes to complete
    for p in processes:
        p.join()

    # Write collected data to CSV
    data_flights = "data_flights.csv"
    with open(data_flights, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(time_data)
        writer.writerow(price_data)

    time.sleep(1)
    print(list(time_data))
    print(list(price_data))
    prediction_date = (datetime.strptime(pred_date,"%Y-%m-%d")).strftime("%m-%d-%Y") 
    predicted_price = pred.main(prediction_date)
    if predicted_price is not None:
        solution_update(predicted_price)