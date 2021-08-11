from googlehelper import SpreadQuery
from configurationhelper import ManageDate
from datetime import date


class Main:
    pass


class Sync(SpreadQuery):
    def check_updated(self):
        self.new_managed_date = ManageDate()
        check_uptodate = self.new_managed_date.check_last_update()
        if not check_uptodate:
            self.autosync()

    def autosync(self):
        list_of_ids = self.new_managed_date.downloaded_list()

    def buttonsync(self):
        pass


