import json
import requests
import os


def get_json_write_csv_for_countries(url_country, path_country_csv):
    try:
        print('Buscando json...')
        response_country = requests.get(url_country, timeout=6000)
        response_country.raise_for_status()

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.TooManyRedirects as errm:
        print(errm)
    except requests.ConnectionError as errc:
        print(errc)
    except requests.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

    countries = json.loads(response_country.text)

    print("Criando csv com dados dos países...")
    if os.path.exists(path_country_csv):
        print('Existe arquivo dados csv países. Removendo...')
        os.remove(path_country_csv)

    with open(path_country_csv, 'a', encoding="utf-8") as file:
        for c in countries:
            csv = f'{c.get("Country")};{c.get("ISO2")}\n'
            file.write(csv)
    print("Pronto")


def init(path_country_csv):
    print('Carga json dados COVID-19 iniciada.')
    print()

    url_country = r'https://api.covid19api.com/countries'

    get_json_write_csv_for_countries(url_country, path_country_csv)

    print()
    print('Carga json finalizada.')
