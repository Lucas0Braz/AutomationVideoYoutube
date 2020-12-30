import datetime as dt
import time
import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd

class SpreedsheetCommunication():

    def __init__(self, credentials='./automacaovideos-c5ce8eea03a2.json', key_spreedsheet='1LWnbn69ut4qxXKoDTpFXLH6mgEHWhrBRiJRKoUpISEU'):
        self.credentials = credentials
        self.key_spreedsheet = key_spreedsheet


    def get_df_spreedsheet(self):
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials, scope)

        gc = gspread.authorize(credentials)

        wks = gc.open_by_key(self.key_spreedsheet)

        worksheet = wks.get_worksheet(0)

        data = worksheet.get_all_values()
        headers = data.pop(0)

        df = pd.DataFrame(data, columns=headers)
        return df

    def update_spreedsheet(self):
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        pass





