from urllib.parse import urlparse
from typing import Dict, List

class MystenLoader:
    def extract_address_by_type(self, data: List[List[str]], type_: str) -> List[str]:
        # Filter out empty rows and header row
        filtered_data = [row for row in data if len(row) != 0 and row[0] != 'Type']
        addresses = []

        for row in filtered_data:
            # Ensure row has enough columns and matches the type
            if row[0] == type_ and len(row) >= 3:
                address = row[2].strip()
                # Skip empty addresses
                if not address:
                    continue
                    
                if type_ in ('NFT', 'Coin', 'Object'):
                    # For NFT/Coin/Object types, address must contain '::'
                    if '::' in address:
                        addresses.append(address)
                elif type_ == 'Package':
                    # For Package type, address must not contain '::'
                    if '::' not in address:
                        addresses.append(address)
                elif type_ == 'Domain':
                    # Add http:// prefix if missing
                    if not address.startswith(('http://', 'https://')):
                        address = 'http://' + address
                    try:
                        # Extract and validate hostname
                        hostname = urlparse(address).hostname
                        if hostname:
                            addresses.append(hostname.lower())
                    except Exception as e:
                        print(f"Invalid URL for Domain: {address} Error: {e}")
        return addresses

    def process_sheet_data(self, spreadsheet_data: List[List[str]]) -> Dict[str, List[str]]:
        return {
            'coin': self.extract_address_by_type(spreadsheet_data, 'Coin'),
            'object': self.extract_address_by_type(spreadsheet_data, 'NFT') +
                     self.extract_address_by_type(spreadsheet_data, 'Object'),
            'package': self.extract_address_by_type(spreadsheet_data, 'Package'),
        }
