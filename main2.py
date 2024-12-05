import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
import serpapi

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

# Specify the desired timeouts
desired_timeout = 60  # Timeout in seconds

# Specify the Chrome browser driver with desired timeouts
driver = webdriver.Chrome(
    executable_path=driver_path,
    options=chrome_options,
    service_log_path=os.devnull,  # Disable logging
    service_args=["--verbose", f"--connect-timeout={desired_timeout}", f"--read-timeout={desired_timeout}"]
)

# Open the provided website
driver.get("https://msbte.org.in/pcwebBTRes/pcResult01/pcfrmViewMSBTEResult.aspx")
print("Website opened successfully.")

# Enter the enrollment number
enrollment_number = "2212270229"  # Change this to the desired enrollment number
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

#click print
print_button=driver.find_element(By.XPATH,"/html/body/form/div[5]/div[1]/div[2]/button")

#click print_to_save
print_to_save=driver.find_element(By.XPATH,"/html/body/print-preview-app//print-preview-sidebar//print-preview-button-strip//div/cr-button[1]")

