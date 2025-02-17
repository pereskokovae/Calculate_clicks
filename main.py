import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def shorten_link(long_url, token):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    payload = {
        "access_token": token,
        "url": long_url,
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
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    if netloc == 'vk.cc':
        return True
    else:
        return False


if __name__ == "__main__":
    token = os.environ['TOKEN']
    long_url = input("Введите ссылку: ")


    try:
        if is_shorten_link(long_url):
            short_link_part = long_url.split('/')[-1]
            clicks_count = count_clicks(short_link_part, token)
            print('Количество кликов по сокращенной ссылке:', clicks_count)
        else:
            short_link = shorten_link(long_url, token)
            print('Сокращенная ссылка:', short_link)
     
            short_link_part = short_link.split('/')[-1]
            clicks_count = count_clicks(short_link_part, token)
            print('Количество кликов по сокращенной ссылке:', clicks_count)

    except requests.exceptions.HTTPError as err:
        print(f"Ошибка при обращении к API, проверте на наличие ошибок: {err}")





















        

