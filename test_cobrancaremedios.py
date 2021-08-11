import unittest
from gerar_cobranca_remedios import Fatura
from cobrança_faturas import NovaFatura


class TesteRemedios(unittest.TestCase):
    def setUp(self) -> None:
        self.new_invoice = Fatura()
        self.reader = self.new_invoice.ler_nome_valor()
        self.fatura = NovaFatura(nome_cao="Cassio", mespassed="Agosto", hotel=True)
        self.fatura1 = NovaFatura(nome_cao="Cassio", mespassed="Agosto", hotel=False)

    def test_novafatura(self):
        self.fatura.monta_fatura()
        self.fatura1.monta_fatura()



if __name__ == '__main__':
    unittest.main()
