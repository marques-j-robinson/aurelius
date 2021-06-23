import requests


BASE_URL = 'https://stoic-server.herokuapp.com'


def format_quote(req):
    body    = req['body']
    author  = req['author']
    source  = req['quotesource']
    res = body + '\n'
    res += f'-{author}, {source}'
    return res


def get_quote():
    r = requests.get(f'{BASE_URL}/random')
    reqs = r.json()
    return format_quote(reqs[0])
