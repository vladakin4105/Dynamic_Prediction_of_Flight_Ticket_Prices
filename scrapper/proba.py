from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurare WebDriver
driver = webdriver.Chrome()  # Înlocuiește cu path-ul către ChromeDriver dacă e nevoie
driver.get("https://www.google.com/flights")

# Așteaptă încărcarea paginii
wait = WebDriverWait(driver, 10)

try:
    # Selectează opțiunea dus-întors
    round_trip_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="Round trip"]'))
    )
    round_trip_button.click()

    # Introdu locația de plecare
    departure_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Where from?"]'))
    )
    departure_field.clear()
    departure_field.send_keys("Bucharest")  # Exemplu: București
    departure_field.send_keys(Keys.ENTER)

    # Introdu locația de destinație
    destination_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Where to?"]'))
    )
    destination_field.clear()
    destination_field.send_keys("Paris")  # Exemplu: Paris
    destination_field.send_keys(Keys.ENTER)

    # Selectează data de plecare
    departure_date_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Departure date"]'))
    )
    departure_date_field.click()
    time.sleep(1)  # Așteaptă să se deschidă calendarul
    departure_date = driver.find_element(By.XPATH, '//div[@aria-label="March 10, 2024"]')  # Înlocuiește cu data dorită
    departure_date.click()

    # Selectează data de întoarcere
    return_date = driver.find_element(By.XPATH, '//div[@aria-label="March 20, 2024"]')  # Înlocuiește cu data dorită
    return_date.click()

    # Dă click pe butonul de căutare
    search_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Search")]'))
    )
    search_button.click()

    print("Căutarea a fost inițiată cu succes!")

except Exception as e:
    print("Eroare:", e)

finally:
    # Închide driverul după câteva secunde
    time.sleep(10)
    driver.quit()
