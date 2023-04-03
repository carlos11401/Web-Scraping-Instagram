# install chromedriver automatically
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