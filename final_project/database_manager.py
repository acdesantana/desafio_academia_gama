import pyodbc
import requests
from datetime import datetime


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


def insert_data(cursor):
    endpoint_country = "https://api.covid19api.com/countries"
    countries = get_data_from_api(endpoint_country)

    insert_row_counter = 0
    countries_with_error = ["Lesotho", "Poland", "United Arab Emirates",
                            "Cook Islands", "Peru", "Qatar",
                            "Mayotte", "Montserrat", "Uzbekistan",
                            "Germany", "Isle of Man", "Equatorial Guinea",
                            "Croatia", "Gibraltar", "Argentina", "Australia",
                            "Colombia", "Finland", "Guinea", "Samoa", "Cyprus",
                            "Hong Kong, SAR China", "Saint-Barthélemy", "South Georgia and the South Sandwich Islands",
                            "Sudan", "Viet Nam", "Guam", "Malawi", "Pakistan",
                            "Bhutan", "Greenland", "Jamaica", "Myanmar",
                            "Rwanda", "Trinidad and Tobago", "United States of America", "Cameroon",
                            "Canada", "Guinea-Bissau", "Belize", "Chile", "Kenya", "Marshall Islands", "Réunion",
                            "Bolivia", "Burkina Faso", "Montenegro", "Tonga", "Azerbaijan", "Bahamas", "Latvia",
                            "Morocco", "Swaziland", "Tuvalu", "Bahrain", "Botswana", "Nicaragua", "Paraguay", "Armenia",
                            "Brazil", "Kuwait", "Netherlands Antilles", "Wallis and Futuna Islands", "Uruguay", "Egypt",
                            "Gambia", "Mongolia", "Pitcairn", "South Sudan", "Switzerland", "Namibia",
                            "Northern Mariana Islands", "Saint Kitts and Nevis", "Sweden", "Iraq", "Israel",
                            "Nauru", "Norway", "Sao Tome and Principe", "Macao, SAR China", "Nigeria", "Panama",
                            "Albania", "Belarus", "Serbia", "El Salvador", "Ireland", "Oman", "Palestinian Territory",
                            "Seychelles", "Somalia", "Barbados", "Falkland Islands (Malvinas)",
                            "Saint Vincent and Grenadines", "Syrian Arab Republic (Syria)"]

    for country in countries:

        if country['Country'] in countries_with_error:
            try:
                # cursor.execute("INSERT INTO COUNTRY VALUES (?,?,?)", country['Country'], country['ISO2'], country['Slug'])
                # insert_row_counter += 1
                # cursor.execute("SELECT @@IDENTITY AS ID;")
                # country_id = cursor.fetchone()[0]
                country_id = 0
                cursor.execute("SELECT * FROM COUNTRY WHERE SLUG=?", country['Slug'])
                country_id = cursor.fetchone()[0]

                current_date = datetime.now().isoformat()
                endpoint_country_data = f"https://api.covid19api.com/country/{country['Slug']}?" \
                                        f"from=2020-01-01T00:00:00Z&to={current_date}T00:00:00Z"
                country_covid = get_data_from_api(endpoint_country_data)

                if country_id != 0:
                    for covid in country_covid:
                        modified_date = covid['Date'].split('T', 1)[0]
                        selected_day = modified_date.split('-')[2]
                        today = datetime.today().date()

                        if modified_date in ['2020-01-07', '2020-01-15', '2020-12-15', '2021-01-07', '2021-01-15']:
                            try:
                                # insert confirmed (Case Type 1)
                                cursor.execute("INSERT INTO COUNTRY_COVID_DAILY_CASES VALUES (?,?,?,?)",
                                               (country_id, 1, covid['Confirmed'], covid['Date']))
                                insert_row_counter += 1

                                try:
                                    # insert deaths (Case Type 2)
                                    cursor.execute("INSERT INTO COUNTRY_COVID_DAILY_CASES VALUES (?,?,?,?)",
                                                   (country_id, 2, covid['Deaths'], covid['Date']))
                                    insert_row_counter += 1

                                except Exception as e:
                                    cursor.rollback()
                                    print(f'Erro de insert na Tabela COUNTRY_COVID_DAILY_CASES '
                                          f'do país {country["Country"]}. Erro encontrado: {e}')

                            except Exception as er:
                                cursor.rollback()
                                print(f'Erro de insert na Tabela COUNTRY_COVID_DAILY_CASES '
                                      f'do país {country["Country"]}. Erro encontrado: {er}')

                            print(f"{country['Country']} dia {covid['Date'].split('T', 1)[0]} salvos...")

            except Exception as err:
                cursor.rollback()
                print(f'Erro de insert na Tabela COUNTRY do país {country["Country"]}. Erro encontrado: {err}')

            print(f"Dados do país {country['Country']} salvos com sucesso...")

    print(f'Inseridos {insert_row_counter} registros inseridos no banco de dados.')


def opens_connection():
    try:
        # second connection available for testing
        """pyodbc.connect('Driver={SQL Server};'
                              'Server=sqlservergama.database.windows.net;'
                              'Database=db1;'
                              'UID=hanna;'
                              'PWD=P@ssw0rd;',
                              autocommit=True)"""

        # connection being used
        return pyodbc.connect('Driver={SQL Server};'
                              'Server=sqlcovid19.database.windows.net;'
                              'Database=DB_COVID_NINETEEN;''UID=datarangers;'
                              'PWD=data_rangers19;',
                              autocommit=True)

    except Exception as e:
        print(f'Erro ao conectar no SQL Server.', e)


def opens_cursor():
    connection = opens_connection()
    return connection, connection.cursor()


print(f'Iniciando execução do script Covid-19')
time_ini = datetime.now()

print('Testando conexão com o banco...')
conn, global_cursor = opens_cursor()
print("Conexão com o banco realizada com sucesso...")

print('Carga no banco iniciada...')
insert_data(global_cursor)
global_cursor.close()
conn.close()
print('Carga no banco finalizada.')

elapsed = datetime.now() - time_ini
print(f'Execução do script finalizada. Tempo gasto: {elapsed}')
