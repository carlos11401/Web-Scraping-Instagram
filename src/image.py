# install chromedriver automatically
import os
import requests

class Images:
    def __init__(self, list_images):
        self.list_images = list_images

    def download(self):
        print(">> Downloading images...")
        try:
            for url in self.list_images:
                response = requests.get(url)
                number = self.list_images.index(url) + 1
                image_name = 'img/image'+str(number)+'.jpg'
                with open(image_name, 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            print(">> Error downloading images. Error: ", e)

        print(">> Images downloaded. Total:", len(self.list_images))

    def delete(self):
        if self.list_images == []:
            print(">> No images to delete.")
            return
        print(">> Deleting images...")
        try:
            for url in self.list_images:
                number = self.list_images.index(url) + 1
                image_name = 'img/image'+str(number)+'.jpg'
                os.remove(image_name)
        except Exception as e:
            print(">> Error deleting images. Error: ", e)
            
        print(">> Images deleted. Total:", len(self.list_images))

    def set_images_url(self, list_images):
        self.list_images = list_images