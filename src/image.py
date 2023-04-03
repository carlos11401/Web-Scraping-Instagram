# install chromedriver automatically
import requests

class Images:
    def __init__(self, list_images):
        self.list_images = list_images
        
    def download(self):
        print(">> Downloading images...")
        for url in self.list_images:
            response = requests.get(url)
            number = self.list_images.index(url)
            image_name = 'image'+str(number)+'.jpg'
            with open(image_name, 'wb') as f:
                f.write(response.content)

        print(">> Images downloaded. Total:", len(self.list_images))