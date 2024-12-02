from urllib.parse import urlparse
from typing import Dict, List

class MystenLoader:
    def extract_address_by_type(self, data: List[List[str]], type_: str) -> List[str]:
        filtered_data = [row for row in data if len(row) != 0 and row[0] != 'Type']
        addresses = []

        for row in filtered_data:
            if row[0] == type_:
                if type_ in ('NFT', 'Coin', 'Object'):
                    if '::' in row[2]:
                        addresses.append(row[2])
                elif type_ == 'Package':
                    if '::' not in row[2]:
                        addresses.append(row[2])
                elif type_ == 'Domain':
                    if not row[2].startswith(('http://', 'https://')):
                        row[2] = 'http://' + row[2]
                    try:
                        hostname = urlparse(row[2]).hostname.lower()
                        row[2] = hostname
                        addresses.append(row[2])
                    except Exception as e:
                        print(f"Invalid URL for Domain: {row[2]} Error: {e}")
        return addresses

    def process_sheet_data(self, spreadsheet_data: List[List[str]]) -> Dict[str, List[str]]:
        return {
            'coin': self.extract_address_by_type(spreadsheet_data, 'Coin'),
            'object': self.extract_address_by_type(spreadsheet_data, 'NFT') +
                     self.extract_address_by_type(spreadsheet_data, 'Object'),
            'package': self.extract_address_by_type(spreadsheet_data, 'Package'),
        }
