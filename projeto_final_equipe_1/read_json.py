import json
import requests
import os


def get_json_write_csv_for_countries(url_country, path_country_json, path_country_csv):
    if not os.path.isfile(path_country_json):
        print('Arquivo json de países não existe. ')
        try:
            print('Buscando json...')
            response_country = requests.get(url_country, timeout=6000)
            response_country.raise_for_status()

            print('Escrevendo arquivo json spaíses...')
            with open(path_country_json, 'w+', encoding="utf-8") as json_country:
                json_country.write(response_country.text)

            print('Pronto.')
            print()
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

    with open(path_country_json, 'r', encoding="utf-8") as c:
        countries = json.loads(c.read())

    print("Criando csv com dados dos países...")
    if os.path.exists(path_country_csv):
        print('Existe arquivo dados csv países. Removendo...')
        os.remove(path_country_csv)

    with open(path_country_csv, 'a', encoding="utf-8") as file:
        for c in countries:
            csv = f'{c.get("Country")};{c.get("ISO2")}\n'
            file.write(csv)
    print("Pronto")


def get_json_write_csv_for_summary(url_summary, path_summary_json, path_summary_csv):
    if not os.path.isfile(path_summary_json):
        print('Arquivo json de sumário países não existe. ')
        try:
            print('Buscando json...')
            response_summary = requests.get(url_summary, timeout=60)
            response_summary.raise_for_status()

            print('Escrevendo arquivo json com sumário spaíses...')
            with open(path_summary_json, 'w+', encoding="utf-8") as json_summary:
                json_summary.write(response_summary.text)

            print('Pronto.')
            print()
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

    with open(path_summary_json, 'r', encoding="utf-8") as c:
        countries = json.loads(c.read())

    list_summary_countries = countries.get('Countries')

    print("Criando csv com dados sumários dos países...")
    if os.path.exists(path_summary_csv):
        print('Existe arquivo dados csv sumário países. Removendo...')
        os.remove(path_summary_csv)

    with open(path_summary_csv, 'a', encoding="utf-8") as file:
        for c in list_summary_countries:
            json_summary_country = c.get('Country')
            json_summary_country_code = c.get('CountryCode')
            json_summary_country_id = c.get('ID')
            csv = f'{json_summary_country};{json_summary_country_code}\n'
            file.write(csv)
    print("Pronto")


def init(path_country_csv, path_summary_csv):
    print('Carga json dados COVID-19 iniciada.')
    print()

    url_country = r'https://api.covid19api.com/countries'
    path_country_json = r'/home/amanda/Documents/Accademia_Accenture/Desafio/projeto_final_equipe_1/json/countries.json'

    url_summary = r'https://api.covid19api.com/summary'
    path_summary_json = r'/home/amanda/Documents/Accademia_Accenture/Desafio/projeto_final_equipe_1/json/summary.json'

    get_json_write_csv_for_summary(url_summary, path_summary_json, path_summary_csv)
    get_json_write_csv_for_countries(url_country, path_country_json, path_country_csv)

    print()
    print('Carga json finalizada.')
