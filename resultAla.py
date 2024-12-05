import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def open_website():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://msbte.org.in/pcwebBTRes/pcResult01/pcfrmViewMSBTEResult.aspx")

open_website()

captcha_image_url = driver.find_element(By.ID, "imgCaptcha").get_attribute("src")
print(captcha_image_url)

def download_image(url, filepath):
    response = requests.get(url)
    with open(filepath, 'wb') as file:
        file.write(response.content)

image_path = 'captcha.png'
download_image(captcha_image_url, image_path)

def getcaptcha(file_path, overlay=False, api_key='K83764332088957', language='eng'):
    """ OCR.space API request with local file.
    :param file_path: Image file path.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """
    
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(file_path, 'rb') as file:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={file_path: file},
                          data=payload,
                          )
    return str(r.content.decode())

print(getcaptcha(image_path))
