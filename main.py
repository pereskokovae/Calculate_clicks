import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


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


def count_clicks(shorten_link, token):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    payload = {
        "access_token": token,
        "key": shorten_link,
        "v": "5.199",
        "interval": "forever"
    }
    response = requests.get(api_url, params=payload)
    response.raise_for_status()
    stats = response.json()['response']['stats']
    return stats[0]['views']


def is_shorten_link(short_link_part, token):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    payload = {
        "access_token": token,
        "key": short_link_part,
        "v": "5.199",
        "interval": "forever"
    }
    response = requests.get(api_url, params=payload)
    response.raise_for_status()
    
    link_stats = response.json()
    return 'error' not in link_stats


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description='Сокращение ссылок и подсчет кликов.')
    parser.add_argument('long_url', type=str, help='Длинная ссылка для сокращения')
    args = parser.parse_args()

    token = os.environ['TG_TOKEN']
    long_url = args.long_url
    url = urlparse(long_url)

    try:
        key = url.path.lstrip('/')

        if is_shorten_link(key, token):
            clicks_count = count_clicks(key, token)
            print('Количество кликов по сокращенной ссылке:', clicks_count)
        else:
            short_link = shorten_link(long_url, token)
            print('Сокращенная ссылка:', short_link)
    except requests.exceptions.HTTPError as err:
        print(f"Ошибка при обращении к API, проверьте правильность ввода: {err}")


if __name__ == "__main__":
    main()
