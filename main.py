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


def is_shorten_link(short_link_part, token):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    payload = {
        "access_token": token,
        "key": short_link_part,
        "v": "5.199",
        "interval": "forever"
    }
    try:
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        data = response.json()
        
        if 'error' in data:
            return False
        else:
            return True
    
    except requests.RequestException:
        return False


def main():
    load_dotenv()
    
    token = os.environ['TG_TOKEN']
    long_url = input("Введите ссылку: ")
    url = urlparse(long_url)

    try:
        if is_shorten_link(long_url, token):
            clicks_count = count_clicks(long_url, token)
            print('Количество кликов по сокращенной ссылке:', clicks_count)
        else:
            short_link = shorten_link(long_url, token)
            print('Сокращенная ссылка:', short_link)
    except requests.exceptions.HTTPError as err:
        print(f"Ошибка при обращении к API, проверьте правильность ввода: {err}")


if __name__ == "__main__":
    main()


