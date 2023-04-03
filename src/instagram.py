# install chromedriver automatically
import os
import pickle
import sys
# selenium driver
# define type of element to search
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec # conditions to wait for
from selenium.common.exceptions import TimeoutException # exception to handle
# instagram credentials
from src.config_ig import *
from src.chrome import *
from src.image import Images

class Instagram:
    def __init__(self):
        chrome = Chrome()
        chrome.init()

        self.instagram_url = 'https://www.instagram.com'
        self.instagram_robots_url = 'https://www.instagram.com/robots.txt'
        
        self.driver = chrome.driver
        self.wait = chrome.wait
        
        self.cookies_file = 'instagram.cookies'
    
    def start(self):
        if not self.login():
            print('>> Login unsuccessful')
            input('>> Press any key to continue...')
            self.driver.quit()
            sys.exit(1)


        hashtag = input('>> Enter a hashtag: #')
        number_of_images = int(input('>> Enter number of images to download: '))
        images_url = self.get_images_url(hashtag, number_of_images)
        images = Images(images_url)
        images.download()
        input('>> Press any key to continue...')

    def login(self):
        if os.path.exists(self.cookies_file):
            response = self.login_by_cookies()
            return response
        else:
            response = self.manual_login()
            return response

    def manual_login(self):
        print('>> Manual logging in ...')
        self.driver.get(self.instagram_url)
        try:
            # text box for username
            element = self.wait.until(ec.visibility_of_element_located((By.NAME, 'username'))) # wait for element to appear
            element.send_keys(USER_IG)

            # text box for password
            element = self.wait.until(ec.visibility_of_element_located((By.NAME, 'password'))) # wait for element to appear
            element.send_keys(PASSWORD_IG)

            # button to login
            element = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))) # wait for element to appear
            element.click()

            # button to save information
            element = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//button[text()="Save Info"]'))) # wait for element to appear
            element.click()

            # test if login was successful
            element = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'article[role="presentation"]'))) # wait for element to appear
            print('>> Login successful')

        except TimeoutException:
            print('>> ERROR!!! Element not found')
            return False
        
        print('>> Saving cookies...')
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open('instagram.cookies', 'wb'))
        print('>> Cookies saved.')
        return True

    def login_by_cookies(self):
        try:
            print('>> Logging in by cookies...') 
            cookies = pickle.load(open(self.cookies_file, 'rb'))
            self.driver.get(self.instagram_robots_url)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.driver.get(self.instagram_url)
            print('>> Login successful')
            return True
        except:
            print('>> ERROR!!! Cookies not found')
            return False

    def get_images_url(self, hashtag, number_of_images):   
        print('>> Getting images url...')     
        
        self.driver.get(f'{self.instagram_url}/explore/tags/{hashtag}/')
        url_list = []
        count_url = 0
        while len(url_list) < number_of_images:
            elements = self.wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._aagv')))
        
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

            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        
        print('>> Images url obtained.')
        return url_list