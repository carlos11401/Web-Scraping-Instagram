# install chromedriver automatically
import os
import pickle
import sys
from webdriver_manager.chrome import ChromeDriverManager
# selenium driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# define type of element to search
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # wait for element
from selenium.webdriver.support import expected_conditions as ec # conditions to wait for
from selenium.common.exceptions import TimeoutException # exception to handle
# instagram credentials
from src.config_ig import *


class Chrome:
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def init(self):
        # Use the ChromeDriverManager to get the latest version of the ChromeDriver executable and install it
        path = ChromeDriverManager(path='./chromedriver').install()

        myOptions = self.get_chromeOptions()
        myService = Service(path) 
        
        driver = webdriver.Chrome(service=myService, options=myOptions)
        driver.set_window_position(0, 0)
        self.wait = WebDriverWait(driver, 10)
        self.driver = driver
    
    def get_chromeOptions(self):
        # Set up Chrome options
        options = Options()

        # Set the user agent for the browser
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--window-size=1000,1000')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-notifications')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--log-level=3')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--no-first-run')
        options.add_argument('--no-proxy-server')
        options.add_argument('--disable-blink-features=AutomationControlled')

        exp_options = [
                        'enable-automation', 
                        'ignore-certificate-errors', 
                        'enable-logging'
                        ]
        options.add_experimental_option('excludeSwitches', exp_options)

        preferences = {
                        'profile.default_content_setting_values': 2,
                        'intl.accept_languages': ['es-ES', 'es'],
                        'credentials_enable_service': False
                    }
        options.add_experimental_option('prefs', preferences)
        return options