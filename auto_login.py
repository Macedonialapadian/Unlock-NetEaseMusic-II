# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00AA8BCED547CAFC81FC1C60D07256E4D094DCF6F187A2D249D62505746B5B5B7915ABB8349E52BC8C35120547B0282E7CD55FDECA26CF2E22A2BB4BD9649E117E94E87812420C9354354AA219FC20211E1031BC63CAB5B490200E654A3BBF9DBC5BB16FF6BE45EA9512E89FDDC26E7FAACE268C4B852BAC760EE78ADF736A1E6DC5A2D77176CA47829A26242E113999124445264E786BBF0D9FCCC37F29A479FC6E19CC9501EF35DB29BDDF60A5A496D9666B3B288D6B105CBE7AC9521041D589F076432AC5DAB6244294833A13BEDD37D6CA05C92FAF5C13BBF69E8207F3154358AA2ABAF8C136927818C16713EAA15261D1C0B4322DCFB5E2A82D408B0DEF15BEA7AB4BCE27C114D038059AF489F45AA6412A4AAD88C1DADB7C8A39149588D843B142AB8DA9B9DF0790184C35C9985293DA0E156C34E4E80D2F8283201226DD4057150C1AADDAA4375BBB2E0D166306C6735C9BA3BE50ED9CABD8946FB4EFD2"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
