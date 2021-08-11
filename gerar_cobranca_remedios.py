import json
import locale
from datetime import date
import calendar
from locale import LC_ALL, setlocale
setlocale(LC_ALL, "pt_br")
mes = calendar.month_name[date.today().month]


class Fatura:

    def __init__(self, nome="Todos"):
        self.nome = nome

    def ler_nome_valor(self):
        with open(f"files/tables/Remedios_{mes}.json") as arquivo_remedios:
            leitor = json.load(arquivo_remedios)
            for row in leitor:
                yield row

    def nome_pais(self):
        for row in self.ler_nome_valor():
            if row['Total'] != 'R$ 000':
                if row['Pais'] == 'Nome Não Encontrado':
                    greeting = "Olá!"
                else:
                    nome_pais = row['Pais']
                    greeting = f"Olá {nome_pais}!"

                yield greeting, row

    def invoice_builder(self):
        for greeting, related_dictionary in self.nome_pais():
            try:
                total = "{:.2f}".format(int(related_dictionary['Total'].split("$")[1])/100)
            except IndexError:
                break

            medicamento = "Duprantel"

            fatura_remedios = f'''
{greeting}!

*O Pet Park está iniciando o teste*
*para o envio separado para pagamento das medicações.*
(Em caso de problemas, favor contactar: Cássio)

O medicamento tomado foi o {medicamento}!

Para o peso de {related_dictionary['Cliente']} o valor foi:

{'='*30}
*Total*: R${total}
{'='*30}

O feedback desse teste é muito importante. 
Por favor, nos faça saber se a mudança é bem-vinda.

O Pet Park agradece à todos pela confiança
'''
            yield fatura_remedios
if __name__ == '__main__':
    nova_fatura = Fatura()
    for row in nova_fatura.ler_nome_valor():
        gerador = nova_fatura.invoice_builder()
        for each in gerador:
            print(each)
            with open(f"remedios_{mes}", "a+") as f:
                f.write(each)



    # gerador = nova_fatura.nome_pais()
    # gerador = nova_fatura.ler_nome_valor()
    #         for e in gerador:
    #             print(e)