import pyodbc
from datetime import date, datetime


def insert_country_summary(c, summary_csv):
    with open(summary_csv, 'r', encoding="utf-8") as csv:
        for linha in csv:
            dado = linha.rstrip().split(';')
            try:
                #   usar o ISO2 como key no dict = {ISO2 : id} criado na funcao anterior
                c.execute("INSERT INTO COUNTRY_COVID_DATA VALUES (?, ?, ?, ?, ?, ?, ?)", dado)

            except Exception as e:
                c.rollback()
                print('Erro insert Países Summary.', dado, e)


def insert_country(c, country_csv):
    print(f'Iniciando carga na tabela COUNTRY.')
    with open(country_csv, 'r', encoding="utf-8") as csv:
        for linha in csv:
            dado = linha.rstrip().split(';')
            try:
                c.execute("INSERT INTO COUNTRY VALUES (?, ?) ", dado)
         #recuperar o id num dict = {ISO2 : id} pra usar ao inserir country_summary

            except Exception as e:
                c.rollback()
                print('Erro insert Países ISO2.', dado, e)

    c.execute('select count(*) from COUNTRY')
    data = c.fetchone()
    print(f'Inseridos {data[0]} registros na tabela COUNTRY.')


def create_database_tables(c):
    your_database_name = "DB_COVID_NINETEEN"
    c.execute("SELECT name FROM master.dbo.sysdatabases where name=?;", (your_database_name,))
    data = c.fetchall()

    if data:
        print('Excluindo banco existente...')
        try:
            c.execute(f'alter database {your_database_name} set single_user with rollback immediate')

            sql_drop = (
                "DECLARE @sql AS NVARCHAR(MAX);"
                "SET @sql = 'DROP DATABASE ' + QUOTENAME(?);"
                "EXEC sp_executesql @sql"
            )
            c.execute(sql_drop, your_database_name)
            c.commit()
        except Exception as e:
            print('Erro ao excluir banco de dados', e)

    else:
        print('Criando banco...')
        try:
            c.execute('CREATE DATABASE DB_COVID_NINETEEN;')
            c.execute('USE DB_COVID_NINETEEN;')
        except Exception as e:
            print('Erro ao criar banco de dados', e)

        print('Criando tabelas...')
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
        except Exception as e:
            print('Erro ao criar tabelas', e)


def open_connection():
    try:
        return pyodbc.connect('Trusted_Connection=no;'
                                'Driver={ODBC Driver 17 for SQL Server};'
                                'Server=localhost;'
                                'Database=master;'
                                'UID=sa;'
                                'PWD=s3nha_SQLServ3r;',
                                autocommit=True)
    except Exception as e:
        print(f'Erro ao conectar no SQL Server.', e)


def open_cursor():
    connection = open_connection()
    return connection, connection.cursor()


def init(path_country_csv, path_summary_csv):
    conn, cursor = open_cursor()

    print()
    print('Carga no banco iniciada.')
    create_database_tables(cursor)

    insert_country_summary(cursor, path_summary_csv)
    insert_country(cursor, path_country_csv)

    conn.close()

    print('Carga no banco finalizada.')
