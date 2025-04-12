import calendar
from datetime import datetime  # Importação corrigida
import requests
from colorama import init, Fore, Style

# Comando para inicializar o colorama (colorir o terminal)
init()

# Função para buscar os feriados nacionais.
def buscar_feriados(ano):
    url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()

        # Corrigindo para chamar .json() corretamente
        feriados = resposta.json()

        # Verifique o formato da resposta para entender o que está vindo
        print(feriados)  # Imprime os dados recebidos para debug

        # Criando um dicionário com a chave como tupla (dia, mês) e valor o nome do feriado
        return {(int(f["date"][8:10]), int(f["date"][5:7])): f["name"] for f in feriados}
    
    except Exception as e:
        print("X Erro ao buscar feriados online:", e)
        return {}

# Função para mostrar o calendário do ano
def Mostrar_calendario_ano(ano, feriados_todos):
    print(f"\n Calendário do Ano {ano}\n")

    for mes in range(1, 13):
        print(f"\n{calendar.month_name[mes]} {ano}".center(28, "-"))  # Nome do mês
        print("Dom Seg Ter Qua Qui Sex Sáb")

        cal = calendar.monthcalendar(ano, mes)

        for semana in cal:
            for dia in semana:
                if dia == 0:
                    print("  ", end=" ")
                elif (dia, mes) in feriados_todos:
                    # Exibe o dia do feriado em vermelho
                    print(Fore.RED + f"{dia:2d}" + Style.RESET_ALL, end=" ")
                else:
                    print(f"{dia:2d}", end=" ")

            print()

    # Exibe a lista dos feriados
    print("\nFeriados em", ano)
    for (dia, mes), nome in sorted(feriados_todos.items()):
        data_formatada = f"{dia:02d}/{mes:02d}"
        print(f"{data_formatada} - {nome}")

# Função principal
def main():
    try:
        ano = int(input("Digite o ano para exibir no calendário: "))

        if ano <= 0:
            raise ValueError

        # Buscar os feriados e montar um set de tuplas (dia, mês)
        feriados_todos = buscar_feriados(ano)

        if not feriados_todos:
            print("Não foi possível recuperar os feriados.")
            return

     

        Mostrar_calendario_ano(ano, feriados_todos)

    except ValueError:
        print("Por favor, digite um ano válido (número inteiro positivo).")

# Entrada do script
if __name__ == "__main__":
    main()





