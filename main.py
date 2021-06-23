import random

from lib.aws import S3, format_title
from lib.instagram import Instagram, get_hashtags
from lib.stoic import get_quote


BUCKET_NAME = 'mrp-paintings'
IMG_PATH = 'painting.jpg'

instagram = Instagram()
s3 = S3()
all_paintings = s3.get_objects(BUCKET_NAME)
total = len(all_paintings)


def build_caption():
    idx = random.randrange(total)
    painting = all_paintings[idx]
    s3.download_file(BUCKET_NAME, painting.key, IMG_PATH)
    res = f'{format_title(painting.key)}\n\n'
    res += f'{get_quote()}\n\n'
    res += get_hashtags()
    return res


def cleanup():
    os.remove(f'{IMG_PATH}.REMOVE_ME')


if __name__ == '__main__':
    caption = build_caption()
    instagram.login()
    instagram.post(IMG_PATH, caption)
    cleanup()
