from webdriver_manager.chrome import  ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.by import By

def init_chrome():
    path = ChromeDriverManager(path='./chromedriver').install()

    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
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
    # 
    exp_options = [
                    'enable-automation', 
                    'ignore-certificate-errors', 
                    'enable-logging'
                    ]
    options.add_experimental_option('excludeSwitches', exp_options)
    #
    preferences = {
                    'profile.default_content_setting_values': 2,
                    'intl.accept_languages': ['es-ES', 'es'],
                    'credentials_enable_service': False
                }
    options.add_experimental_option('prefs', preferences)

    myService = Service(path)
    driver = webdriver.Chrome(service=myService, options=options)
    return driver

if __name__ == '__main__':
    driver = init_chrome()
    url = 'https://www.instagram.com'
    
    driver.get(url)
    input('Press any key to continue...')
    driver.quit()