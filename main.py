import os
import glob
import random

import requests
import boto3
from instabot import Bot
from dotenv import load_dotenv
load_dotenv()


IG_USERNAME = os.environ.get('IG_USERNAME')
IG_PASSWORD = os.environ.get('IG_PASSWORD')


s3 = boto3.resource('s3')
BUCKET_NAME = 'mrp-paintings'
primary_bucket = s3.Bucket(BUCKET_NAME)
bucket_items = primary_bucket.objects.all()
objects = list(bucket_items)
total = len(objects)
HASHTAGS = '#art #oilpainting #landscape #landscapepainting #philosophy #stoic #bobross'
img_path = 'painting.jpg'


def generate_random_num():
    return random.randrange(total)


def get_title(item):
    return item.key.split('.')[0].replace('-', ' ').title()


def get_random_painting():
    cur_id = generate_random_num()
    obj = objects[cur_id]
    s3_client = boto3.client('s3')
    s3_client.download_file(BUCKET_NAME, obj.key, img_path)
    return obj


def get_quote():
    r = requests.get('https://stoic-server.herokuapp.com/random')
    r = r.json()
    return r[0]


def create_post():
    painting = get_random_painting()
    title = get_title(painting)

    quote = get_quote()
    author = quote['author']
    quotesource = quote['quotesource']

    raw_post = ''
    raw_post += f'{title}\n\n'
    raw_post += quote['body'] + '\n'
    raw_post += f'-{author}, {quotesource}\n\n'
    raw_post += HASHTAGS
    return raw_post


if __name__ == '__main__':
    cookie_del = glob.glob('config/*cookie.json')
    os.remove(cookie_del[0])
    api = Bot()
    api.login(username=IG_USERNAME, password=IG_PASSWORD)
    caption = create_post()
    api.upload_photo(img_path, caption)
