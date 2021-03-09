/* PROJETO FINAL - ACCADEMIA ACCENTURE/GAMA ACADEMY
 * Turma 5 - Engenharia de Dados
 * Grupo 1 - DataRangers: Alciso Filho, Amanda Campos, Gustavo Galisa, Hanna Corr�a, J�ssica Santos, Lucas Aurelio, 
 * Rafaela Muniz, Stephany Mackyne e Willian Higa.
 * Data de entrega: 13/03/2021
 * Descri��o do c�digo: cria��o de tabelas de pa�ses e casos confirmados e mortos por Covid-19 desde 01/01/2020 
 * em banco de dados alocado no Azure.
 */

CREATE DATABASE DB_COVID_NINETEEN;

USE DB_COVID_NINETEEN;

CREATE TABLE COUNTRY (
	ID	INT		NOT NULL IDENTITY(1, 1),
	NAME	VARCHAR(50)	NOT NULL,
	ISO2	VARCHAR(2)	NOT NULL,
	CONSTRAINT PK_COUNTRY PRIMARY KEY (ID)
);

CREATE TABLE COUNTRY_COVID_DATA (
	ID			INT	NOT NULL IDENTITY(1, 1),
	ID_COUNTRY		INT	NOT NULL,
	NEW_CONFIRMED		INT	NOT NULL, 
	TOTAL_CONFIRMED		INT	NOT NULL,
	NEW_DEATHS		INT	NOT NULL, 
	TOTAL_DEATHS		INT	NOT NULL,
	DATE			DATE	NOT NULL,
	CONSTRAINT PK_COUNTRY_COVID_DATA PRIMARY KEY (ID),
	CONSTRAINT FK_COUNTRY_COVID_DATA_COUNTRY FOREIGN KEY (ID_COUNTRY)
	REFERENCES COUNTRY (ID)
);