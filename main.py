import urllib.parse
import urllib.request

from google_play_scraper import app

PACKAGE_CONFIGS = ['com.dertefter.wearfiles-en-us', 'com.dertefter.neticlient-ru-ru']


def download_badge(label, message, color, logo_name, filename):
    clean_label = label.replace('-', '--').replace('_', '__')
    clean_message = message.replace('-', '--').replace('_', '__')

    encoded_label = urllib.parse.quote(clean_label)
    encoded_message = urllib.parse.quote(clean_message)

    url = f"https://img.shields.io/badge/{encoded_label}-{encoded_message}-{color}?style=for-the-badge"

    if logo_name:
        url += f"&logo={logo_name}&logoColor=white"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Бейдж успешно сохранен: {filename}")
    except Exception as e:
        print(f"Не удалось скачать бейдж {filename}: {e}")


def get_for_package_config(package_config):
    parts = package_config.rsplit('-', 2)

    if len(parts) == 3:
        package_name, lang, country = parts
    else:
        print(f"Ошибка: Неверный формат строки '{package_config}'. Используйте формат 'package.name-lang-country'")
        return

    print(f"\nПолучение данных для {package_name} (Язык: {lang}, Страна: {country})...")
    try:
        result = app(package_name, lang=lang, country=country)

        downloads_count = result['installs']
        downloads_filename = f"{package_name}_downloads.svg"
        download_badge(
            label="Downloads",
            message=downloads_count,
            color="095943",
            logo_name="google-play",
            filename=downloads_filename
        )

        score = result['score'] if result['score'] is not None else 0.0

        filled_stars_count = max(0, min(5, round(score)))
        empty_stars_count = 5 - filled_stars_count

        stars_string = ('★' * filled_stars_count) + ('☆' * empty_stars_count)
        rating_text = f"{stars_string}"

        rating_filename = f"{package_name}_rating.svg"
        download_badge(
            label="",
            message=rating_text,
            color="095943",
            logo_name="google-play",
            filename=rating_filename
        )

    except Exception as e:
        print(f"Произошла ошибка с пакетом {package_name}: {e}")


for config in PACKAGE_CONFIGS:
    get_for_package_config(config)