from selenium.common.exceptions import UnexpectedAlertPresentException
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
import serpapi
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def getcaptcha(captcha_link):
    params = {
        "engine": "google_lens",
        "url": captcha_link,
        "api_key": "cd6996b4cfb86e240a63a87dab59f14044e2166d682f09a911afd1729a028d2a"
    }

    search = serpapi.search(params)
    results = search.as_dict()

    text_result = results["text_results"][0]["text"]
    return text_result

# Path to the Chrome browser executable
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# Path to the Chrome browser driver (chromedriver)
driver_path = "C:/Users/SID/Desktop/SID/python/Webscrapper/chromedriver.exe"

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path
chrome_options.add_argument("--start-maximized")

# Specify the Chrome browser driver
service = Service(driver_path)

# Initialize the Chrome browser with specified options
driver = webdriver.Chrome(service=service, options=chrome_options)

def open_website():
    driver.get("https://msbte.org.in/pcwebBTRes/pcResult01/pcfrmViewMSBTEResult.aspx")
    print("Website opened successfully.")

def fill_info(enum):
    # Enter the enrollment number
    enrollment_input = driver.find_element(By.ID, "txtEnrollOrSeatNo")
    enrollment_input.clear()
    enrollment_input.send_keys(enum)
    print("Enrollment number entered successfully:", enum)

    # Select the third option in the dropdown
    dropdown = Select(driver.find_element(By.ID, "ddlEnrollOrSeatNo"))
    dropdown.select_by_index(2)  # Index starts from 0, so index 2 is the third option
    print("Dropdown option selected successfully.")

def download_result(start_enum, end_enum):
    for enum in range(start_enum, end_enum + 1):
        open_website()
        while True:
            captcha_image_url = driver.find_element(By.ID, "imgCaptcha").get_attribute("src")
            if captcha_image_url == "https://msbte.org.in/pcwebBTRes/pcZTemp/pcCaptchaHot.png":
                print("Captcha Not Found, Reloading...")
                driver.refresh()
                print("Page reloaded successfully.")
                time.sleep(2)
            else:
                print("CAPTCHA image URL:", captcha_image_url)
                break

        fill_info(enum)

        # Extract CAPTCHA text from SerpApi response
        captcha_text = getcaptcha(captcha_image_url)

        print("Extracted CAPTCHA text:", captcha_text)

        # Enter the CAPTCHA text
        captcha_input = driver.find_element(By.ID, "txtCaptchaHot")
        print("CAPTCHA input field found.")
        captcha_input.send_keys(captcha_text)
        print("CAPTCHA text entered successfully.")

        # Click on the 'Submit' button
        submit_button = driver.find_element(By.XPATH, "/html/body/form/div[4]/div[2]/div/div/div[5]/div[2]/input[5]")
        submit_button.click()
        print("Submit button clicked successfully.")

        # Wait for the result page to load
        time.sleep(5)  # Adjust the wait time as needed

        try:
            # Get the HTML source code of the webpage
            html_source = driver.page_source

            # Define the directory where you want to save the webpage
            save_path = "C:/Users/SID/Desktop/SID/python/Webscrapper/Result/"

            # Generate the file name using the enrollment number
            file_name = str(enum) + ".html"

            # Save the HTML source code to a file
            with open(save_path + file_name, "w", encoding="utf-8") as file:
                file.write(html_source)

            print("Webpage saved successfully as:", file_name)

        except UnexpectedAlertPresentException:
            # Handle the alert here
            alert = driver.switch_to.alert
            alert_text = alert.text
            print("Alert Text:", alert_text)
            alert.accept()  # Close the alert
            print("Alert accepted.")

            # Optionally, you can add code here to handle the situation where the result data is not found
            print("Result data not found for enrollment number:", enum)

            # Skip this iteration
            continue

start_enum = int(input("Enter starting enrollment number: "))
end_enum = int(input("Enter ending enrollment number: "))

download_result(start_enum, end_enum)

driver.quit()
