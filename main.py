from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  # Import NoSuchElementException
import requests

import pytesseract
from PIL import Image
from io import BytesIO

# Path to the Chrome browser executable
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# Path to the Chrome browser driver (chromedriver)
driver_path = "C:/Users/SID/Desktop/SID/python/Webscrapper/chromedriver.exe"

# Path to Tesseract executable (you may need to adjust this path based on your installation)
pytesseract.pytesseract.tesseract_cmd = 'C:/Users/SID/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path
chrome_options.add_argument("--start-maximized")

# Specify the Chrome browser driver
service = Service(driver_path)

try:
    # Initialize the Chrome browser with specified options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the provided website
    driver.get("https://msbte.org.in/pcwebBTRes/pcResult01/pcfrmViewMSBTEResult.aspx")
    print("Website opened successfully.")

    try:
        # Enter the enrollment number
        enrollment_number = "123"  # Change this to the desired enrollment number
        enrollment_input = driver.find_element(By.ID, "txtEnrollOrSeatNo")
        enrollment_input.send_keys(enrollment_number)
        print("Enrollment number entered successfully:", enrollment_number)

        # Select the third option in the dropdown
        dropdown = Select(driver.find_element(By.ID, "ddlEnrollOrSeatNo"))
        dropdown.select_by_index(2)  # Index starts from 0, so index 2 is the third option
        print("Dropdown option selected successfully.")

        # Get the URL of the CAPTCHA image
        captcha_image_url = driver.find_element(By.ID, "imgCaptcha").get_attribute("src")
        print("CAPTCHA image URL:", captcha_image_url)

        # Download the CAPTCHA image
        response = requests.get(captcha_image_url)
        print("Response status code:", response.status_code)
        captcha_image = Image.open(BytesIO(response.content))
        captcha_image.save("captcha.png")
        print("CAPTCHA image downloaded and saved successfully.")

        # Perform OCR on the captcha image
        captcha_text = pytesseract.image_to_string(captcha_image, lang='eng', config='--psm 6')

        print("Extracted CAPTCHA text:", captcha_text)

        # Enter the captcha text
        captcha_input = driver.find_element(By.ID, "txtCaptchaHot")
        print("CAPTCHA input field found.")
        captcha_input.send_keys(captcha_text)
        print("CAPTCHA text entered successfully.")

    except NoSuchElementException as e:
        print("Error: Could not find the dropdown, image, or input element.")
        print(e)

except Exception as e:
    print("Error: An unexpected error occurred while initializing the browser.")
    print(e)
