import os
import base64
import json
from urllib.parse import urlparse
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import shutil
from loader.mysten import MystenLoader
from loader.suiet import SuietLoader

class SpreadsheetUpdater:
    def __init__(self, spreadsheet_id, credentials_base64, loader, range_='Sheet1!A:H', output_dir='../dist'):
        self.spreadsheet_id = spreadsheet_id
        self.credentials_base64 = credentials_base64
        self.loader = loader
        self.range_ = range_
        self.output_dir = output_dir
        self.credentials = self._load_credentials()
        self.service = self._build_service()

    def _load_credentials(self):
        credentials_json = base64.b64decode(self.credentials_base64).decode('utf-8')
        credentials_info = json.loads(credentials_json)
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        return Credentials.from_service_account_info(credentials_info, scopes=scopes)

    def _build_service(self):
        return build('sheets', 'v4', credentials=self.credentials)

    def fetch_upstream_sheet(self):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_
        ).execute()
        spreadsheet_data = result.get('values', [])
        return self.loader.process_sheet_data(spreadsheet_data)

    def update_file(self, spreadsheet_data):
        for type_, addresses in spreadsheet_data.items():
            file_path = os.path.join(
                os.path.dirname(__file__),
                self.output_dir,
                f'{type_.lower()}-list.json'
            )
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f'Read {type_}-list.json successfully.')
            except Exception as e:
                print(f'Error reading file for {type_}: {e}')
                continue

            updated_blocklist = sorted(set(data.get('blocklist', []) + addresses))
            data['blocklist'] = updated_blocklist

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                    print(f'{type_}-list.json updated successfully.')
            except Exception as e:
                print(f'Error writing file for {type_}: {e}')

    def run(self):
        sheet_data = self.fetch_upstream_sheet()
        self.update_file(sheet_data)

if __name__ == '__main__':
    credentials_base64 = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_BASE64')
    mysten_spreadsheet_id = os.environ.get('MYSTEN_SPREEDSHEET_ID')
    suiet_spreadsheet_id = os.environ.get('SUIET_SPREEDSHEET_ID')

    snapshot_dir = './snapshot'
    dist_dir = './dist'

    # mkdir dist directory if not exists
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    # load the snapshot files to dist directory
    for filename in os.listdir(snapshot_dir):
        full_file_name = os.path.join(snapshot_dir, filename)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dist_dir + '/' + filename)
            print(f'Copied {filename} to {dist_dir}')

    # Update from Mysten sheet
    mysten_updater = SpreadsheetUpdater(
        spreadsheet_id=mysten_spreadsheet_id,
        credentials_base64=credentials_base64,
        loader=MystenLoader()
    )
    mysten_updater.run()

    # Update from Suiet sheet
    suiet_updater = SpreadsheetUpdater(
        spreadsheet_id=suiet_spreadsheet_id,
        credentials_base64=credentials_base64,
        loader=SuietLoader(),
        range_='Sheet1!A:F'  # Adjust range for Suiet sheet format
    )
    suiet_updater.run()
