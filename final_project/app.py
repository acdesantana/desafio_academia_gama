import streamlit as st
import pandas as pd
import pyodbc
import seaborn as sns


def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=sqlcovid19.database.windows.net;'
                            'Database=DB_COVID_NINETEEN;''UID=datarangers;'
                            'PWD=data_rangers19;')

    cursor = conn.cursor()

    query_covid = 'SELECT * FROM COUNTRY_COVID_DAILY_CASES'
    query_country = 'SELECT * FROM COUNTRY'

    df_data = pd.read_sql(query_covid, conn)
    df_country = pd.read_sql(query_country, conn)



    df_geral = pd.merge(df_data, df_country, left_on='ID_COUNTRY', right_on='ID')
    df_geral.drop(['ID_x', 'ID_y', 'ISO2', 'SLUG'], axis=1)
    df_geral = df_geral[['DATE', 'ID_COUNTRY', 'NAME', 'ID_CASE_TYPE', 'TOTAL_CASES']]

    df_geral['DATE'] = pd.to_datetime(df_geral['DATE'], infer_datetime_format=True)
    df_geral.set_index('DATE', inplace=True)

    df_casos = df_geral.loc[df_geral['ID_CASE_TYPE'] == 1, :]
    df_mortes = df_geral.loc[df_geral['ID_CASE_TYPE'] == 2, :]

    top_casos = df_casos.groupby(['NAME'])['TOTAL_CASES'].agg(['sum']).sort_values('sum', ascending=False).head(
        10).index.to_list()
    top_mortes = df_mortes.groupby(['NAME'])['TOTAL_CASES'].agg(['sum']).sort_values('sum', ascending=False).head(
        10).index.to_list()

    st.title('Projeto final - Gama Academy')

    menu = ['Descrição', 'Casos confirmados - diário', 'Mortes por COVID - diário', 'Mortes por COVID - total', 'Casos confirmados - total']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Descrição':
        st.subheader('Descrição')

        st.write('''
        Armazenamento de dados d COVID-19 de todos os países do mundo através da API: https://documenter.getpostman.com/view/10808728/\n
        1) Crie um Script SQL para criação de um DataBase com um Schema para armazenar os registros de países e os dados de COVID-19 por todo o mundo. Na tabela que será armazenada os dados de países, 2 campos são obrigatórios de serem consistidos:\n
        - Nome do país\n
        - Código ISO2\n
        Em outros repositórios devem ser armazenados a quantidade de casos confirmados e mortes de cada um dos países do mundo, desde o dia 01/01/2020.\n
        2) Crie um banco de dados relacional no provedor de nuvem Azure para armazenamento dos dados em questão, estabelecidos pelo script com o dito schema, criado na etapa anterior. O banco de dados pode ser SQL Server, MySQL, MariaDB, Postgres ou algum outro SQL.
        3) Desenvolva um script Python que faça leitura da API determinada no enunciado inicial desta atividade para realizar o armazenamento de países e dos casos confirmados e de mortes da COVID-19. O armazenamento destas informações deverá ser em BD SQL, consistido no Azure através do schema definido na etapa 1 desta atividade.\n
        Após armazenamento dos valores no BD, este dito script Python deverá retornar as seguintes informações em tela, caso o usuário escolha:\n
        1) Panorama diário de quantidade de casos confirmados de COVID-19 dos 10 países do mundo com maiores números.\n
        2) Panorama diário de quantidade de mortes de COVID-19 dos 10 países do mundo com números.\n
        3) Total de mortes por COVID-19 dos 10 países do mundo com maiores números.\n
        4) Total de casos confirmados por COVID-19 dos 10 países do mundo com maiores números.\n
        A impressão das 4 informações citadas acima deverá acontecer em tela, através do prompt de comando de execução do programa.
        ''')

    elif choice == 'Casos confirmados - diário':
        st.subheader('Casos confirmados - diário')
        st.write('Panorama diário de quantidade de casos confirmados de COVID-19 dos 10 países do mundo com maiores números.')
        df_q1 = df_casos.loc[df_casos['NAME'].isin(top_casos), :]
        sns.set(rc={'figure.figsize': (11.7, 8.27)})
        sns.lineplot(x="DATE", y="TOTAL_CASES", hue="NAME", ci=None, linewidth = 2.5, data= df_q1)
        st.pyplot()

    elif choice == 'Mortes por COVID - diário':
        st.subheader('Casos confirmados - diário')
        st.write('Panorama diário de quantidade de mortes de COVID-19 dos 10 países do mundo com números.')
        df_q2 = df_mortes.loc[df_mortes['NAME'].isin(top_mortes), :]
        sns.set(rc={'figure.figsize': (11.7, 8.27)})
        sns.lineplot(x="DATE", y="TOTAL_CASES", hue="NAME", ci=None, linewidth=2.5, data=df_q2)
        st.pyplot()

    elif choice == 'Mortes por COVID - total':
        st.subheader('Número total de mortes por COVID')
        st.write('Total de mortes por COVID-19 dos 10 países do mundo com maiores números.')
        st.write(pd.DataFrame(cursor.execute('''SELECT top 10 nome, max(total_cases) as total FROM (
                                                        SELECT *, Row_Number() OVER (PARTITION BY nome ORDER BY total_cases DESC) AS rn
                                                        FROM (SELECT 
                                                                    con.name as nome,
                                                                    ccdc.TOTAL_CASES as total_cases
                                                                    FROM COUNTRY_COVID_DAILY_CASES ccdc
                                                                    join COUNTRY con on con.ID = ccdc.ID_COUNTRY 
                                                                    where ccdc.ID_CASE_TYPE = 2
                                                                    Group by con.name, total_cases
                                                                ) as Q1 
                                                        ) AS Q2
                                                WHERE rn <= 10
                                                group by nome
                                                ORDER BY total desc;''')))

    elif choice == 'Casos confirmados - total':
        st.subheader('Casos confirmados - total')
        st.write('Total de casos confirmados por COVID-19 dos 10 países do mundo com maiores números')
        st.write(pd.DataFrame(cursor.execute('''SELECT top 10 nome, max(total_cases) as total FROM (
                                                        SELECT *, Row_Number() OVER (PARTITION BY nome ORDER BY total_cases DESC) AS rn
                                                        FROM (SELECT 
                                                                    con.name as nome,
                                                                    ccdc.TOTAL_CASES as total_cases
                                                                    FROM COUNTRY_COVID_DAILY_CASES ccdc
                                                                    join COUNTRY con on con.ID = ccdc.ID_COUNTRY 
                                                                    where ccdc.ID_CASE_TYPE = 1
                                                                    Group by con.name, total_cases
                                                                ) as Q1 
                                                        ) AS Q2
                                                WHERE rn <= 10
                                                group by nome
                                                ORDER BY total desc;''')))


if __name__ == '__main__':
    main()