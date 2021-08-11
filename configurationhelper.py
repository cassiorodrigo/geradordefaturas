import configparser
from configparser import ConfigParser
from datetime import date
import json
file = "config.ini"

SSs_ids_to_sync = ["1gzcSxg4fO5aG7pxhTxROaQZcQWuqVlKfrBdB0Te87jM",
                   "1ziTC08U4kEP-1PsCQYX4yeJGEh6Oeg6q72yLNxu8QQc",
                   "1Etl6qAPpMUWqG1VF3sqWtStUjIQp-NPEAw4pw0m21ew",
                   "1xkggka2yJdZQGHkzp5pqXFoLazwVforAdZ7_byHJyrk"]


class ManageDate(ConfigParser):

    def __init__(self,  *args, **kwargs):
        super().__init__(self)
        self.read('config.ini')

    def update_last_sync(self):
        try:
            self.set('Last_Updated', 'last_sync', date.today().strftime('%d/%m/%Y'))
        except configparser.NoSectionError:
            self.add_section('Last_Updated')
        finally:
            self.set('Last_Updated', 'last_sync', date.today().strftime('%d/%m/%Y'))

        with open(file, "w") as confile:
            self.write(confile)

        return date.today().strftime('%d/%m/%Y')

    def check_last_update(self):
        self.read('config.ini')
        last_up = self.get('Last_Updated', 'last_sync')
        today = date.today().strftime('%d/%m/%Y')
        if last_up < today:
            return False
        return True

    def registrar_sheets_baixadas(self):

        try:
            titulos_baixadas = self.get('Sheets_baixadas', "titulos_sincronizadas")
            ids_baixadas = self.get('Sheets_baixadas', "ids_sincronizadas")
        except configparser.NoSectionError:
            self.add_section('Sheets_baixadas')
        finally:
            # self.set('Sheets_baixadas', 'titulos_sincronizadas', titulo)
            self.set('Sheets_baixadas', 'ids_sincronizadas', json.dumps(SSs_ids_to_sync))
            with open('config.ini', 'w') as f:
                self.write(f)
        self.read('config.ini')

    def downloaded_list(self):
        self.read('config.ini')
        downloaded_lists = json.loads(self.get('Sheets_baixadas', "ids_sincronizadas"))
        return downloaded_lists


if __name__ == '__main__':
    # ManageDate().update_last_sync()
    if not ManageDate().check_last_update():
        print('atualizar e rodar updatelastcheck e registrar_sheets_baixadas')
    new_object = ManageDate()
    new_object.registrar_sheets_baixadas()
    print(new_object.downloaded_list())

