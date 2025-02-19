import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import os.path


def shorten_link(url, token):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    payload = {
        "access_token": token,
        "url": url,
        'v': '5.199'
    }

    response = requests.get(api_url, params=payload)
    response.raise_for_status()  

    short_url = response.json()['response']['short_url']
    return short_url


def count_clicks(short_link_part, token):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    payload = {
        "access_token": token,
        "key": short_link_part,
        "v": "5.199",
        "interval": "forever"
    }

    response = requests.get(api_url, params=payload)
    response.raise_for_status()

    count_click = response.json()['response']['stats']
    return count_click


def is_shorten_link(url):
    return url.netloc == 'vk.cc'


def get_short_link_part(url, token):
    return os.path.basename(url.path) if is_shorten_link(url) else os.path.basename(shorten_link(url.geturl(), token))


if __name__ == "__main__":
    load_dotenv()

    token = os.environ['TOKEN']
    long_url = input("Введите ссылку: ")
    url = urlparse(long_url)


    try:
        short_link_part = get_short_link_part(url, token)
        clicks_count = count_clicks(short_link_part, token)
        print('Количество кликов по сокращенной ссылке:', clicks_count)
    except requests.exceptions.HTTPError as err:
        print(f"Ошибка при обращении к API, проверьте на наличие ошибок: {err}")














        

