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
#
instagram_url = 'https://www.instagram.com'
instagram_robots_url = 'https://www.instagram.com/robots.txt'

# Define a function to initialize a Chrome WebDriver instance
def init_chrome():
    # Use the ChromeDriverManager to get the latest version of the ChromeDriver executable and install it
    path = ChromeDriverManager(path='./chromedriver').install()

    # Set up Chrome options
    options = Options()

    # Set the user agent for the browser
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'
    options.add_argument(f'user-agent={user_agent}')

    # Set the window size
    options.add_argument('--window-size=1000,1000')

    # Disable web security
    options.add_argument('--disable-web-security')

    # Disable extensions
    options.add_argument('--disable-extensions')

    # Disable notifications
    options.add_argument('--disable-notifications')

    # Ignore certificate errors
    options.add_argument('--ignore-certificate-errors')

    # Disable the sandbox
    options.add_argument('--no-sandbox')

    # Set the log level
    options.add_argument('--log-level=3')

    # Allow running insecure content
    options.add_argument('--allow-running-insecure-content')

    # Disable default browser check
    options.add_argument('--no-default-browser-check')

    # Disable first run
    options.add_argument('--no-first-run')

    # Disable proxy server
    options.add_argument('--no-proxy-server')

    # Disable Blink features
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

    myService = Service(path) 
    driver = webdriver.Chrome(service=myService, options=options)
    driver.set_window_position(0, 0)
    return driver

def login_instagram():
    

    if os.path.exists('instagram.cookies'):
        print('>> Logging in by cookies...')
        print('>> Cookies found')
        
        cookies = pickle.load(open('instagram.cookies', 'rb'))
        driver.get(instagram_robots_url)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        driver.get(instagram_url)
        print('>> Login successful')
        return True
    
    print('>> Logging in ...')
    driver.get(instagram_url)
    try:
        # text box for username
        element = wait.until(ec.visibility_of_element_located((By.NAME, 'username'))) # wait for element to appear
        element.send_keys(USER_IG)

        # text box for password
        element = wait.until(ec.visibility_of_element_located((By.NAME, 'password'))) # wait for element to appear
        element.send_keys(PASSWORD_IG)

        # button to login
        element = wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))) # wait for element to appear
        element.click()

        # button to save information
        element = wait.until(ec.element_to_be_clickable((By.XPATH, '//button[text()="Save Info"]'))) # wait for element to appear
        element.click()

        # test if login was successful
        element = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'article[role="presentation"]'))) # wait for element to appear
        print('>> Login successful')

    except TimeoutException:
        print('>> ERROR!!! Element not found')
        return False
    
    cookies = driver.get_cookies()
    pickle.dump(cookies, open('instagram.cookies', 'wb'))
    print('>> Cookies saved.')
    return True

def download_images():
    driver.get(f'{instagram_url}/explore/tags/python/')
    wait = WebDriverWait(driver, 10)
    
    hashtag = input('>> Enter a hashtag: #')
    number_of_images = int(input('>> Enter number of images to download: '))
    driver.get(f'{instagram_url}/explore/tags/{hashtag}/')

    print('>> Downloading images...')
    url_list = []
    count_url = 0
    while len(url_list) < number_of_images:
        elements = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._aagv')))
        
        for element in elements:
            try:
                url = element.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                if url not in url_list:
                    url_list.append(url)
                    count_url += 1

            except:
                pass
           
        
            if count_url == number_of_images:
                break

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    print('>> Images downloaded. Total:', len(url_list))
    print(len(url_list))
    print(url_list[0])
    print(url_list[1])
    print(url_list[2])
    print(url_list[3])
    print(url_list[4])
    print(url_list)

if __name__ == '__main__':
    driver = init_chrome()
    wait = WebDriverWait(driver, 10) # wait for 10 seconds for element to appear
    res_login = login_instagram()
    if not res_login:
        print('>> Login unsuccessful')
        input('>> Press any key to continue...')
        driver.quit()
        sys.exit(1)
    download_images()
    input('>> Press any key to continue...')
    driver.quit()
    sys.exit(1)



