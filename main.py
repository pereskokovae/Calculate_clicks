import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(url, token):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    payload = {
        "access_token": token,
        "url": url,
        'v': '5.199'
        }
    response = requests.get(api_url, params=payload)
    response.raise_for_status()
    return response.json()['response']['short_url']


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
    return response.json()['response']['stats']


def is_shorten_link(url, token):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    short_link_part = os.path.basename(url.path)
    payload = {
        "access_token": token,
        "key": short_link_part,
        "v": "5.199",
        "interval": "forever"
    }
    try:
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        return True 
    except requests.exceptions.HTTPError:
        return False


def main():
    load_dotenv()

    token = os.environ['TG_TOKEN']
    long_url = input("Введите ссылку: ")
    url = urlparse(long_url)

    try:
        if is_shorten_link(url, token):
            short_link_part = os.path.basename(url.path)
            clicks_count = count_clicks(short_link_part, token)
            print('Количество кликов по сокращенной ссылке:', clicks_count)
        else:
            short_link = shorten_link(url.geturl(), token)
            print('Сокращенная ссылка:', short_link)
    except requests.exceptions.HTTPError as err:
        print(f"Ошибка при обращении к API, проверьте правильность ввода: {err}")


if __name__ == "__main__":
    main()













        

