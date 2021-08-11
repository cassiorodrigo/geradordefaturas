import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from googlehelper import SpreadQuery
from configurationhelper import ManageDate
from datetime import date


class Test (unittest.TestCase):

    def setUp(self) -> None:
        self.new_query_list = ['']
        self.new_configurationtest = ManageDate().update_last_sync()
        self.new_checkdate = ManageDate().check_last_update()
        self.check_today = ManageDate().update_last_sync()
        # self.query_url = SpreadQuery.from_spreadsheets_url(
        # ['https://docs.google.com/spreadsheets/d/1Etl6qAPpMUWqG1VF3sqWtStUjIQp-NPEAw4pw0m21ew/edit#gid=363848394'])
        # self.query_url = SpreadQuery.to_test(
        # ['https://docs.google.com/spreadsheets/d/1Etl6qAPpMUWqG1VF3sqWtStUjIQp-NPEAw4pw0m21ew/edit#gid=363848394'])

    def test_pegar_dados(self):
        # self.assertEqual([''], self.new_query.list_of_ids)
        # self.assertEqual(['1Etl6qAPpMUWqG1VF3sqWtStUjIQp-NPEAw4pw0m21ew'], self.query_url)
        pass

    def test_configparserfile(self):
        self.assertEqual(date.today().strftime("%d/%m/%Y"), self.new_configurationtest)

    def test_checkdatelastup(self):
        self.assertTrue(self.new_checkdate)

    def test_listas_baixadas(self):
        pass

    def test_hoje(self):
        self.assertEqual('05/08/2021', self.check_today)
        self.assertGreater('06/08/2021', self.check_today)


if __name__ == '__main__':
    unittest.main()
