import requests


def get_data_from_api(endpoint):

    try:
        response_country = requests.get(endpoint, timeout=6000).json()
        return response_country

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
