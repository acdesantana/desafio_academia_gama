

class CovidData(object):

    def daily_confirmed(self):
        print('teste 1')

    def total_confirmed(self):
        print('teste 4')

    def daily_deaths(self):
        print('teste 2')

    def total_deaths(self):
        print('teste 3')

    def check_latest_data(self):
        print('teste 5')


def recebeOpcaoUsuario():
    opcao = 0

    print("Bem vindo! Escolha a opção que desejar:\n"
          "1 - Panorama diário da quantidade de casos confirmados de COVID-19 dos 10 países "
          "com maiores índices da pandemia.\n"
          "2 - Panorama diário da quantidade de mortes por COVID-19 dos 10 países "
          "com maiores índices da pandemia.\n"
          "3 - Total de mortes por COVID-19 dos 10 países "
          "com maiores índices da pandemia.\n"
          "4 - Total de casos confirmados de COVID-19 dos 10 países "
          "com maiores índices da pandemia.\n"
          "5 - Sair do Programa\n")

    while opcao < 1 or opcao > 5:
        opcao = int(input("Digite uma opção válida (1 - 5): "))
        if opcao < 1 or opcao > 5:
            print("Opção inválida. Digite novamente")

    return opcao


if __name__ == '__main__':

    covid_status = CovidData()
    print("Entrando no programa...")
    covid_status.check_latest_data()
    opcao = recebeOpcaoUsuario()

    while 1 <= opcao <= 5:
        if opcao == 1:
            covid_status.daily_confirmed()

        elif opcao == 2:
            covid_status.daily_deaths()

        elif opcao == 3:
            covid_status.total_deaths()

        elif opcao == 4:
            covid_status.total_confirmed()

        else:
            print("Você saiu do programa. Obrigado por usar...\n")
            opcao = 6

        if opcao != 6:
            opcao = recebeOpcaoUsuario()


