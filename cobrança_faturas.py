import datetime
import json
pt_months = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes = pt_months[datetime.date.today().month]


class NovaFatura:
    def __init__(self, nome_cao='Todos', mespassed=mes, hotel=True):
        self.nome_cao = nome_cao
        self.mes = mespassed
        self.hotel = hotel

    def get_base(self):
        if not self.hotel:
            with open(f"files/tables/Faturas {self.mes}.json", "r") as table_creche:
                dados_mes = json.load(table_creche)
        else:
            with open(f"files/tables/Faturas Hotel {self.mes}.json", "r") as table_hotel:
                dados_mes = json.load(table_hotel)
        for row_caes in dados_mes:
            if self.nome_cao == row_caes['Cliente']:
                return row_caes

    def get_banhos(self, name_dog_showered):
        lista_dia_de_banhos = []
        with open(f"files/tables/Banhos {self.mes}.json", "r") as banhos_mes:
            banhos_do_mes = json.load(banhos_mes)

            for row_showers in banhos_do_mes:
                if row_showers['Cliente'] == name_dog_showered and row_showers['Banhos'] != '':
                    lista_dia_de_banhos.append(row_showers['Dia do Banho'])
                    how_many_banhos = row_showers['Banhos']
                    how_much_per_banho = row_showers['Cada']
                    total_banhos = row_showers['Total']
                    dias_chuvinha = ' '.join(lista_dia_de_banhos)

                    string_banhos = f'''\nDia(s) do(s) Banho(s): {dias_chuvinha}
                    Quantidade de Banhos: {how_many_banhos}
                    Valor por banho: R${how_much_per_banho:.2f}
                    Total dos Banhos: R${total_banhos:.2f}
                    '''
                else:
                    string_banhos = ''
                    total_banhos = 0

                return string_banhos, total_banhos

    def get_remedios(self, name_dog_medicine):
        with open(f"files/tables/Remedios {self.mes}.json", "r") as remedios_mes:
            remedios_do_mes = json.load(remedios_mes)
            for row_medicine in remedios_do_mes:
                if row_medicine['Cliente'] == name_dog_medicine and row_medicine['Quantidade'] != '':
                    how_many_pills = row_medicine['Quantidade']
                    how_much_per_pill = row_medicine['Valor da Unidade']/100
                    total_pills = row_medicine['Total']/100

                    remedios = f'''\nQuantidade de medicamentos: {how_many_pills}
                    Valor por medicamento: R${how_much_per_pill:.2f}
                    Total medicamentos: R${total_pills:.2f}
                            '''
                else:
                    remedios = ''
                    total_pills = 0
            return remedios, total_pills

    def dias_no_hotel(self):
        if not self.hotel:
            lista_dias_no_hotel = []
            with open("files/tables/Presencas.json", "r") as docpresencas:
                presencas = json.load(docpresencas)
                for presenca in presencas:
                    if presenca['Cliente'] == self.nome_cao and presenca['Hotel/Creche'] != 'Creche':
                        lista_dias_no_hotel.append(presenca['Data'])
                return lista_dias_no_hotel, len(lista_dias_no_hotel)
        else:
            with open(f"files/tables/Faturas Hotel {mes}.json", "r") as dicio_hotel:
                data_hotel = json.load(dicio_hotel)
                for dog_guest in data_hotel:
                    if dog_guest['Cliente'] == self.nome_cao:
                        return dog_guest['Data Entrada'], dog_guest['Data Saída'], dog_guest['Total de Dias']

    def greeting(self):
        nome_cao = self.get_base()
#        if not self.hotel:
        if nome_cao['Cliente'] == self.nome_cao:
            owner = nome_cao['Pais']
            dog = nome_cao['Cliente']
            if owner != "" and owner != 'Nome Não Encontrado':
                nome_dono = f'''Olá {owner}!'''
            else:
                nome_dono = f'''Olá!'''
            greeting = f'''
                {nome_dono} 
                A Pet Fatura de {dog} chegou!

                (Em caso de dúvidas ou erros, contactar Cássio)

                Os métodos de pagamento econtram-se ao final da fatura
        '''
            return greeting

    def monta_fatura(self):
        texto_remedio, total_remedios = self.get_remedios(self.nome_cao)
        texto_banho, total_banho = self.get_banhos(self.nome_cao)
        greeting = self.greeting()
        desconto = 0
        if desconto > 0:
            desconto_string = f'\nDesconto: {desconto}'
        else:
            desconto_string = ''

        termos = f'''Termos de serviço e informações importantes:
                        
                        O cão deve ser entregue com um peitoral ou uma coleira para ajudar na
                        segurança durante as brincadeiras.
                        
                        Horários de Check-in e Check-out:
                            *Das 06h00min até as 09h30min*
                            *Das 12h00min até as 14h00min*
                            *Das 16h30min até as 19h00min*
                            
                        AO CHEGAR, LIGAR A CAMPAINHA LUMINOSA **1 ÚNICA VEZ**
                        (É uma campainha luminosa e logo iremos atender)'''

        hotel = f''' O cão deve levar a ração que está acostumado a comer separada em porções
                        ou com o dosador usualmente utilizado.
                        
                        As notícias sobre a Estadia serão enviadas nos horários padronizados no seguinte 
                        grupo de WhatsApp: 
                         
                        https://chat.whatsapp.com/GQl1TwSLekP1SlADkZb4Qr
                        *Ao Término da estadia, o tutor deve se retirar do grupo.*
                        
                        e fotos no instagram:
                        
                        https://www.instagram.com/petparkcrechehotel/
                         
                        A Localização do Pet Park é:
                    
                        https://maps.app.goo.gl/sZVPac8g8MZtshTR6
                        
                        A Fatura deve ser paga até *1 hora* antes do Check-in'''

        pagamento = f'''Forma de Pagamento:
                                             
                     *PIX*: 39.938.754/0001-22
                     *PicPay*: 
                        https://app.picpay.com/promotionsdetails/495825
                     *Transferência*:
                         Pet Park
                         Banco Nubank
                         Ag.0001
                         C/C: 11466503-4
                         CNPJ: 39.938.754/0001-22 '''
        conclusao = f'''
                        Muito Obrigado!
                        {'-'*20}
                        visite nosso PetSite:
                        www.petparkvv.com.br
                        {'-'*20} '''
        if self.hotel:
            date_in, date_out, total_days = self.dias_no_hotel()
            valor_diaria = 50
            total_hotel = total_days * valor_diaria
            string_hotel = f'''
                        Check-in: {date_in}
                        Check-out: {date_out}
                        Total de dias: {total_days}
                        Valor por diária: R${valor_diaria:.2f}
                        Total Hotel: R${total_hotel:.2f}
            '''
            subtotal = int(total_days) * valor_diaria
            desconto = 0
            total = total_hotel - (total_hotel * desconto / 100)
            vencimento = f'''\nVENCIMENTO = 1 Hora antes do Check-in\n'''
            final = f'''
                        {greeting}
                        {termos}
                        {hotel}
                        {pagamento}
                        {string_hotel}
                        {'='*20}
                        Subtotal: R${subtotal:.2f}
                        {desconto_string}
                        {'+'*20}
                        Total: R${total:.2f}
                        {'+'*20}{vencimento}
                        {'='*20}
                        {conclusao}
                        '''
        else:
            dicio_cao = self.get_base()
            dias_no_hotel, total_dias_no_hotel = self.dias_no_hotel()
            creche = dicio_cao['Valor Creche']
            valor_creche = int(creche.split("$")[1]) / 100
            vencimento = f'''\nVENCIMENTO = 10/{datetime.date.today().month}/{datetime.date.today().year}\n'''
            valor_diaria = 40
            total_hotel = total_dias_no_hotel * valor_diaria
            subtotal = total_remedios + total_banho + total_hotel + valor_creche
            desconto = 0
            total = f'R${subtotal - (subtotal * desconto / 100):.2f}'

            if total_dias_no_hotel == 0:
                comum = ''

            else:
                comum = f'''\n      Dias no Hotel: {', '.join(dias_no_hotel)}
                                    Quantidade de dias: {total_dias_no_hotel}
                                    Valor por diária: R${valor_diaria}
                                    Total Hotel: R$ {total_hotel}'''
            final = f'''
                        {greeting}
                        {termos}
                        {pagamento}
                        
                        Creche: R${valor_creche:.2f}{comum}{texto_remedio}{texto_banho}
                        
                        {'-'*30}
                        Subtotal = R${subtotal:.2f}{desconto_string}
                        {'-'*30}
                        
                        {'+'*20}
                        Total: {total}
                        {'+'*20}{vencimento}
                            {conclusao}
                                    '''
        return final


if __name__ == "__main__":
    nova_fatura = NovaFatura(nome_cao="Dumbledore", hotel=False)
    print(nova_fatura.monta_fatura())
