import gspread
import re
import json
from configurationhelper import ManageDate
import locale
import calendar
import datetime
locale.setlocale(locale.LC_ALL, "pt_br")
mes = calendar.month_name[datetime.date.today().month]

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']
PATH_TO_API_KEY = "files/apikeys/faturasgspread.json"


class SpreadQuery:

    """
    This generates a spreadsheet query and save in a json format file
    called 'responses.json'.
    """

    def __init__(self):
        self.service = gspread.service_account(PATH_TO_API_KEY, scopes=SCOPES)

        if not ManageDate().check_last_update():
            self.update_json_sheets()
        else:
            print('Archive already updated.')

    def update_json_sheets(self):
        new_object = ManageDate()
        for each_id in new_object.downloaded_list():
            openspread = self.service.open_by_key(each_id)
            worksheets = openspread.worksheets()
            for tab in worksheets:
                download = str(input(f'Planilha {openspread.title}\nQuer baixar a tab {tab.title}?\n'
                                     f'["y"/"n"]\n'))
                if download.strip().lower() == 'y':
                    if mes in tab.title:
                        records = openspread.worksheet(tab.title).get_all_records()
                        with open(f"files/tables/{tab.title}.json", "w") as file:
                            file.write('')
                            json.dump(records, file, ensure_ascii=False, indent=4)
                        print(f'Updated {tab.title}')
                ManageDate().update_last_sync()
            else:
                continue

    def update_presencas(self):
        new_object = ManageDate()
        openspread = self.service.open_by_key('1gzcSxg4fO5aG7pxhTxROaQZcQWuqVlKfrBdB0Te87jM')
        records = openspread.worksheet('Presencas').get_all_records()
        with open(f"files/tables/Presencas.json", "w") as file:
            file.write('')
            json.dump(records, file, ensure_ascii=False, indent=4)
        print(f'Updated Presencas')
        ManageDate().update_last_sync()

    def update_banhos(self):
        new_object = ManageDate()
        openspread = self.service.open_by_key('1gzcSxg4fO5aG7pxhTxROaQZcQWuqVlKfrBdB0Te87jM')
        records = openspread.worksheet(f'Banhos {mes}').get_all_records()
        with open(f"files/tables/Banhos_{mes}.json", "w") as file:
            file.write('')
            json.dump(records, file, ensure_ascii=False, indent=4)
        print(f'Updated Banhos')
        ManageDate().update_last_sync()

    def __str__(self):
        pass
        # try:
        #     if self.records:
        #         result = 'Updated file'
        # except AttributeError as aterror:
        #     result = 'File already updated today. No need to update right now'
        # finally:
        #     return result

    def __repr__(self):
        print(f'SpreadQuery()')

    def setup_query(self):
        return

    @classmethod
    def from_spreadsheets_id(cls, list_of_ids):
        return cls()

    @classmethod
    def from_spreadsheets_url(cls, list_of_urls):
        new_ids_list = []
        for each_url in list_of_urls:
            resultado = re.split('/', each_url)
            new_ids_list.append(resultado[5])
        return cls()


if __name__ == "__main__":
    new_query = SpreadQuery()
    new_query.update_json_sheets()
    # new_query.update_banhos()
