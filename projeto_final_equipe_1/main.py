from datetime import datetime
import manage_database_sql_server as sql_server
import read_json


if __name__ == '__main__':
    print(f'Iniciando execução do script Covid-19')
    time_ini = datetime.now()

    path_country_csv = r'/home/amanda/Documents/Accademia_Accenture/Desafio/projeto_final_equipe_1/csv/countries.csv'

    read_json.init(path_country_csv)
    sql_server.init(path_country_csv)

    elapsed = datetime.now() - time_ini
    print(f'Execução do script finalizada. Tempo gasto: {elapsed}')

