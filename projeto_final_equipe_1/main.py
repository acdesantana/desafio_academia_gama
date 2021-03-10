from datetime import datetime
import manage_database_sql_server as sql_server
import read_json


if __name__ == '__main__':
    print(f'Iniciando execução do script Covid-19')
    time_ini = datetime.now()

    path_country_csv = r'/home/amanda/Documents/Accademia_Accenture/Desafio/projeto_final_equipe_1/csv/countries.csv'
    path_summary_csv = r'/home/amanda/Documents/Accademia_Accenture/Desafio/projeto_final_equipe_1/csv/summary.csv'

    read_json.init(path_country_csv, path_summary_csv)
    sql_server.init(path_country_csv, path_summary_csv)

    elapsed = datetime.now() - time_ini
    print(f'Execução do script finalizada. Tempo gasto: {elapsed}')

'''# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
'''