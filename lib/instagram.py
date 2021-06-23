import os
import glob

from instabot import Bot
from dotenv import load_dotenv
load_dotenv()


USERNAME = os.environ.get('IG_USERNAME')
PASSWORD = os.environ.get('IG_PASSWORD')
HASHTAGS = [
    '#art',
    '#artist',
    '#artwork',
    '#artistsoninstagram',
    '#artofinstagram',
    '#painting',
    '#landscape',
    '#landscapepainting',
    '#nature',
    '#oilpainting',
    '#philosophy',
    '#stoicphilosophy',
    '#stoic',
    '#stoicism',
    '#bobross',
    '#marcusaurelius',
]


def get_hashtags():
    return ' '.join(HASHTAGS)


class Instagram:

    def __init__(self):
        """Initialize instance of Bot from instabot."""
        self.api = Bot()

    def clear_cache(self):
        """
        Clear cookie from cache.

        Forces the full login sequence.
        """
        cookie_del = glob.glob('config/*cookie.json')
        os.remove(cookie_del[0])

    def login(self):
        """Login to Instagram."""
        self.clear_cache()
        self.api.login(username=USERNAME, password=PASSWORD)

    def post(self, img_path, caption):
        """
        Post to Instagram.

        Provided with a image path and a caption, will create a new post.
        """
        self.api.upload_photo(img_path, caption)
