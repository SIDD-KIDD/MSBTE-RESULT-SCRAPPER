from PyQt5 import QtCore, QtGui, QtWidgets
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import serpapi
import time
import random

driver = None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(725, 562)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setEnabled(True)
        self.Title.setGeometry(QtCore.QRect(30, 30, 661, 91))
        font = QtGui.QFont()
        font.setPointSize(34)
        self.Title.setFont(font)
        self.Title.setObjectName("Title")
        self.downloadbutton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadbutton.setGeometry(QtCore.QRect(270, 370, 161, 31))
        self.downloadbutton.setObjectName("downloadbutton")
        self.EnterS = QtWidgets.QLabel(self.centralwidget)
        self.EnterS.setGeometry(QtCore.QRect(30, 150, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.EnterS.setFont(font)
        self.EnterS.setObjectName("EnterS")
        self.EnterE = QtWidgets.QLabel(self.centralwidget)
        self.EnterE.setGeometry(QtCore.QRect(30, 220, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.EnterE.setFont(font)
        self.EnterE.setObjectName("EnterE")
        self.StartingEnumBox = QtWidgets.QLineEdit(self.centralwidget)
        self.StartingEnumBox.setGeometry(QtCore.QRect(460, 160, 171, 41))
        self.StartingEnumBox.setObjectName("StartingEnumBox")
        self.EndingEnumBox = QtWidgets.QLineEdit(self.centralwidget)
        self.EndingEnumBox.setGeometry(QtCore.QRect(460, 230, 171, 41))
        self.EndingEnumBox.setObjectName("EndingEnumBox")
        self.locationinput = QtWidgets.QLineEdit(self.centralwidget)
        self.locationinput.setGeometry(QtCore.QRect(460, 290, 171, 41))
        self.locationinput.setObjectName("locationinput")
        self.EnterL = QtWidgets.QLabel(self.centralwidget)
        self.EnterL.setGeometry(QtCore.QRect(30, 280, 251, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.EnterL.setFont(font)
        self.EnterL.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.EnterL.setMouseTracking(False)
        self.EnterL.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.EnterL.setAutoFillBackground(False)
        self.EnterL.setWordWrap(True)
        self.EnterL.setObjectName("EnterL")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect the clicked signal of the download button to a custom slot
        self.downloadbutton.clicked.connect(self.download_results)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Title.setText(_translate("MainWindow", "MSBTE Result Downloader"))
        self.downloadbutton.setText(_translate("MainWindow", "Download Result"))
        self.EnterS.setText(_translate("MainWindow", "Enter Starting Enrollment Num:"))
        self.EnterE.setText(_translate("MainWindow", "Enter Ending Enrollment Num:"))
        self.EnterL.setText(_translate("MainWindow", "Enter Location Where You want to Save The Results:"))

    def get_input_data(self):
        starting_enum = self.StartingEnumBox.text()
        ending_enum = self.EndingEnumBox.text()
        location = self.locationinput.text()
        return starting_enum, ending_enum, location

    def download_results(self):
        start_enum, end_enum, save_path = self.get_input_data()
        mainProg(start_enum, end_enum, save_path)


def getcaptcha(captcha_link):
    params = {
        "engine": "google_lens",
        "url": captcha_link,
        "api_key": "c02cd8befcb177491673d7386dbca156301c348d5412f36c6879b95fe28506ca"
    }
    try:
        search = serpapi.search(params)
        results = search.as_dict()
        print("API response:", results)  # Debugging: print the entire response
        if 'text_results' in results:
            text_results = results['text_results']
            if text_results:
                text_result = text_results[0].get('text', '')
                return text_result
            else:
                print("No text results found in the response.")
                return ""
        else:
            print("'text_results' key not found in the response.")
            return ""
    except Exception as e:
        print(f"Error during API call: {e}")
        return ""



def open_website():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://msbte.org.in/pcwebBTRes/pcResult01/pcfrmViewMSBTEResult.aspx")
    # print("Website opened successfully.")


def fill_info(i_num, captcha_image_url):
    # print("\n\n")
    # print(i_num, ":")
    enrollment_input = driver.find_element(By.ID, "txtEnrollOrSeatNo")
    enrollment_input.clear()
    enrollment_input.send_keys(i_num)
    # print("Enrollment number entered successfully:", i_num)

    dropdown = Select(driver.find_element(By.ID, "ddlEnrollOrSeatNo"))
    dropdown.select_by_index(2)

    captcha_text = getcaptcha(captcha_image_url)
    # print("Extracted CAPTCHA text:", captcha_text)
    captcha_input = driver.find_element(By.ID, "txtCaptchaHot")
    captcha_input.clear()
    captcha_input.send_keys(captcha_text)
    # print("CAPTCHA text entered successfully.")


import random

def download_result(start_enum, end_enum, save_path):
    if not open_website():
        print("Failed to open the website. Exiting...")
        return

    captcha_wrong = False
    enum = int(start_enum)
    max_attempts = 5  # Maximum number of attempts for each enrollment number

    while enum <= int(end_enum):
        Download = False
        attempts = 0
        while True:
            captcha_image_url = driver.find_element(By.ID, "imgCaptcha").get_attribute("src")
            if captcha_image_url == "https://msbte.org.in/pcwebBTRes/pcZTemp/pcCaptchaHot.png":
                driver.refresh()
                time.sleep(2)
            else:
                break

        if captcha_wrong:
            fill_info(enum, captcha_image_url)
            captcha_wrong = False
        else:
            fill_info(enum, captcha_image_url)

        while True:
            try:
                submit_button = driver.find_element(By.XPATH, "/html/body/form/div[4]/div[2]/div/div/div[5]/div[2]/input[5]")
                submit_button.click()

                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.accept()

                if "The Captcha Typed does not match" in alert_text:
                    captcha_wrong = True
                    break
                elif "Result Data not found" in alert_text:
                    Download = True
                    break
                elif "Error in Posted Data" in alert_text:
                    captcha_wrong = True
                    break
            except NoAlertPresentException:
                try:
                    if "Server Error in '/pcwebBTRes' Application." in driver.page_source:
                        raise Exception("Server error detected")

                    html_source = driver.page_source
                    file_name = str(enum) + ".html"
                    with open(save_path + file_name, "w", encoding="utf-8") as file:
                        file.write(html_source)
                    captcha_wrong = False
                    Download = True
                    break
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        print(f"Max attempts reached for enrollment number: {enum}")
                        break
                    print(f"Error downloading result for enrollment number {enum}, attempt {attempts}: {e}")
                    time.sleep(random.uniform(1, 3))  # Wait for a random time before retrying

        if Download:
            enum += 1

    driver.quit()




def mainProg(start_enum, end_enum, save_path):
    global driver
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    driver_path = "C:/Users/SID/Desktop/SID/python/Webscrapper/chromedriver.exe"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument("--start-maximized")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # open_website()
    download_result(start_enum, end_enum, save_path)
    # print("Successfully Downloaded All Results")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
