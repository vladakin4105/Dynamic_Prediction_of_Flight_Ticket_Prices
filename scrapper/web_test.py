from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

# Configure Chromium WebDriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to Chromium WebDriver (installed as `chromium-chromedriver`)
driver = webdriver.Chrome(service=Service("/opt/homebrew/bin/chromedriver"), options=chrome_options)

# Open Chromium, wait 5 seconds, and then close it
try:
    driver.get("https://www.google.com/travel/flights")
    time.sleep(1)
    try:
        accept_button = driver.find_element(By.XPATH, '//span[@jsname="V67aGc" and text()="Accept all"]')
        accept_button.click()
        print("Clicked 'Accept all' button.")
    except Exception as e:
        print("No 'Accept all' button found or error clicking it:", e)
    
    print("Chromium opened successfully!")
    
    time.sleep(1)
    from_location = input("from_location: ")
    input_field = driver.find_element(By.XPATH,'//input[@aria-label="Where from?"]')
    input_field.clear()
    input_field.send_keys(from_location)
    print(f'Entered "{from_location}"')
    time.sleep(1)
    
    
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
    
    time.sleep(0.5)
    
    to_location = input("to_location: ")
    input_to = driver.find_element(By.XPATH, '//input[@aria-label="Where to? "]')
    input_to.clear()  # Clear any pre-filled text
    input_to.send_keys(to_location)
    print(f'entered "{to_location}"')
    
    time.sleep(1)
    
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
    
    time.sleep(1)
    #departure_date = "15-12-2024"    
    #return_date = "7-1-2024"
    #departure and return must be inputs
    #here u must fill the date input fields 
    #tested with webdriver find element ->nu gaseste sau nu poate accesa
    #webdriverwait ->timeout
    #javascript code -->nu modifica
    #problema principala porneste de la faptul ca este un date picker dinamic care impune si ce date sa fie folosite si modifica in timp real arhitectura html ului
    #facand dificila cautarea dupa content/atribute
    try:
        departure_date = input("departure_date(format zz-mm-yyyy): ")
        input_departure_date = driver.find_element(By.XPATH,'//input[@aria-label="Departure"]')
        input_departure_date.clear()
        input_departure_date.send_keys(departure_date)
        input_departure_date.send_keys(Keys.ENTER)
        print(f'Entered "{departure_date}"')
        time.sleep(1)
    except Exception as e:
        print("Eroare la introducerea datei de plecare:", e)

    time.sleep(1)

    try:
        return_date = input("return_date(format zz-mm-yyyy): ")
        input_return_date = driver.find_element(By.XPATH,'//input[@aria-label="Return"]')
        input_return_date.clear()
        input_return_date.send_keys(return_date)
        input_return_date.send_keys(Keys.ENTER)
        print(f'Entered "{return_date}"')
        time.sleep(1)
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
    time.sleep(5)  # Wait to observe changes
    
    time.sleep(3600)
finally:
    driver.quit()
    print("Chromium closed.")

