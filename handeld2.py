from selenium.common.exceptions import UnexpectedAlertPresentException,NoAlertPresentException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import serpapi
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def getcaptcha(captcha_link):
    params = {
        "engine": "google_lens",
        "url": captcha_link,
        "api_key": "a8dc318728493ee313e92d953751864fd7f837eea6a8b42d64c3d2b621df8cd4"
    }

    search = serpapi.search(params)
    results = search.as_dict()

    text_result = results["text_results"][0]["text"]
    return text_result

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
driver_path = "C:/Users/SID/Desktop/SID/python/Webscrapper/chromedriver.exe"

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path
chrome_options.add_argument("--start-maximized")
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def open_website():
    driver.get("https://msbte.org.in/pcwebBTRes/pcResult01/pcfrmViewMSBTEResult.aspx")
    print("Website opened successfully.")

def fill_info(i_num,captcha_image_url):
    print("/n/n")
    print(i_num,":")
    enrollment_input = driver.find_element(By.ID, "txtEnrollOrSeatNo")
    enrollment_input.clear()
    enrollment_input.send_keys(i_num)
    print("Enrollment number entered successfully:", i_num)

    # Select the third option in the dropdown
    dropdown = Select(driver.find_element(By.ID, "ddlEnrollOrSeatNo"))
    dropdown.select_by_index(2)  # Index starts from 0, so index 2 is the third option
    
    # # Extract CAPTCHA text from SerpApi response
    captcha_text = getcaptcha(captcha_image_url)
    print("Extracted CAPTCHA text:", captcha_text)
    captcha_input = driver.find_element(By.ID, "txtCaptchaHot")
    captcha_input.clear()
    captcha_input.send_keys(captcha_text)
    print("CAPTCHA text entered successfully.")

open_website()
def download_result(start_enum, end_enum):
    captcha_wrong = False
    enum = start_enum  
    while enum <= end_enum:
        Download=False
        while True:
            captcha_image_url = driver.find_element(By.ID, "imgCaptcha").get_attribute("src")
            if captcha_image_url == "https://msbte.org.in/pcwebBTRes/pcZTemp/pcCaptchaHot.png":
                print("Captcha Not Found, Reloading...")
                driver.refresh()
                print("Page reloaded successfully.")
                time.sleep(2)
            else:
                print("CAPTCHA Found")
                break

        if captcha_wrong:
            print("Retrying For:", enum)
            fill_info(enum, captcha_image_url)
            captcha_wrong = False  # Reset captcha_wrong after retrying
        else:
            fill_info(enum, captcha_image_url)

        while True:
            try:
                submit_button = driver.find_element(By.XPATH, "/html/body/form/div[4]/div[2]/div/div/div[5]/div[2]/input[5]")
                submit_button.click()
                print("Submit button clicked successfully.")
                # time.sleep(5)

                # Check if the result data is found
                alert = driver.switch_to.alert
                alert_text = alert.text
                print("Alert Text:", alert_text)
                alert.accept()  # Close the alert

                if "The Captcha Typed does not match" in alert_text:
                    print("Captcha is wrong, trying again...")
                    captcha_wrong = True
                    print("captcha_wrong set as True")
                    break
                elif "Result Data not found" in alert_text:

                    print("Result data not found for enrollment number:", enum)
                    Download=True
                    break
                elif "Error in Posted Data" in alert_text:

                    print("Error in posted data, retrying...")
                    captcha_wrong = True
                    break

            except NoAlertPresentException:
                #Result foundd
                html_source = driver.page_source
                save_path = "C:/Users/SID/Desktop/SID/JAVA/webscrapper_java/Result/"
                file_name = str(enum) + ".html"
                with open(save_path + file_name, "w", encoding="utf-8") as file:
                    file.write(html_source)
                print("Webpage saved successfully as:", file_name)
                captcha_wrong = False
                print("Captcha_wrong set as False (result saved successfully).")
                Download=True
                break
        if Download:
            enum += 1
            print("Enum Incremented")

    driver.quit()

start_enum = int(input("Enter starting enrollment number: "))
end_enum = int(input("Enter ending enrollment number: "))

download_result(start_enum, end_enum)
print("Successfully Downloaded All Results")

