import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_driver_selenium(url):
    service = Service(executable_path=ChromeDriverManager().install())
    options = Options()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(10)
    return driver