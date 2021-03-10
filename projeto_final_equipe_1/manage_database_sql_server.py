import pyodbc
from datetime import date, datetime


def insert_country_summary(c, path_summary_csv):
    registros = []

    c.executemany("INSERT INTO COUNTRY_COVID_DATA VALUES (?, ?, ?, ?, ?, ?, ?)", registros)
    c.commit()

def insert_country(c, path_country_csv):
    registros = []

    c.executemany("INSERT INTO COUNTRY VALUES (?, ?, ?)", registros)
    c.commit()


def create_database_tables(c):
    try:
        c.execute('CREATE DATABASE DB_COVID_NINETEEN;')
        c.execute('USE DB_COVID_NINETEEN;')
        c.commit()
    except Exception as e:
        print('Erro ao criar banco de dados', e)

    try:
        c.execute('CREATE TABLE COUNTRY ('
                  'ID		INT				NOT NULL IDENTITY(1, 1), '
                  'NAME	VARCHAR(50)		NOT NULL, '
                  'ISO2	VARCHAR(2)		NOT NULL, '
                  'CONSTRAINT PK_COUNTRY PRIMARY KEY (ID));')

        c.execute('CREATE TABLE COUNTRY_COVID_DATA ( '
                  'ID					INT		NOT NULL IDENTITY(1, 1),'
                  'ID_COUNTRY			INT		NOT NULL, '
                  'NEW_CONFIRMED		INT		NOT NULL, '
                  'TOTAL_CONFIRMED		INT		NOT NULL, '
                  'NEW_DEATHS			INT		NOT NULL, '
                  'TOTAL_DEATHS		INT		NOT NULL, '
                  'DATE				DATE	NOT NULL, '
                  'CONSTRAINT PK_COUNTRY_COVID_DATA PRIMARY KEY (ID), '
                  'CONSTRAINT FK_COUNTRY_COVID_DATA_COUNTRY FOREIGN KEY (ID_COUNTRY) '
                  'REFERENCES COUNTRY (ID));')
        c.commit()
    except Exception as e:
        print('Erro ao criar tabelas', e)


def open_connection():
    try:
        return pyodbc.connect('Trusted_Connection=no;'
                              'Driver={ODBC Driver 17 for SQL Server};'
                              'Server=localhost;'
                              'Database=master;'
                              'UID=sa;'
                              'PWD=s3nha_SQLserv3r;')

    except Exception as e:
        print(f'Erro ao conectar no SQL Server.', e)


def open_cursor():
    connection = open_connection()
    return connection, connection.cursor()


# def init(path_country_csv, path_summary_csv):
print('Carga no banco iniciado.')
print()

path_country_csv = r'/home/amanda/Documents/Accademia_Accenture/Desafio/projeto_final_equipe_1/csv/countries.csv'
path_summary_csv = r'/home/amanda/Documents/Accademia_Accenture/Desafio/projeto_final_equipe_1/csv/summary.csv'

conn, cursor = open_cursor()

create_database_tables(cursor)
insert_country_summary(cursor, path_summary_csv)
insert_country(cursor, path_country_csv)

conn.close()

print()
print('Carga no banco finalizada.')
