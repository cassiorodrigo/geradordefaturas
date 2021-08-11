from cobrança_faturas import NovaFatura
import json
import datetime, calendar
mes = calendar.month_name[datetime.date.today().month]


def cobrar_todos_creche(mes=mes):
    with open(f"files/tables/Faturas {mes}.json", "r") as file:
        data_file = json.load(file)
    for row in data_file:
        if row['Cliente'] != '':
            fatura = NovaFatura(nome_cao=row['Cliente'], hotel=False, mespassed=mes)
            resultado = fatura.monta_fatura()
            with open(f"files/faturas/Faturas {mes}.txt", "a+") as file_faturas:
                file_faturas.write(resultado)
    return True


if __name__=='__main__':
    cobrar_todos_creche('Setembro')
