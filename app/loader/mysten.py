from urllib.parse import urlparse
from typing import Dict, List
import csv
import os

class MystenLoader:
    def __init__(self):
        self.top_domains = self._load_top_domains()

    def _load_top_domains(self) -> set:
        """Load top 1M domains from CSV file"""
        top_domains = set()
        csv_path = os.path.join(
            os.path.dirname(__file__), 
            '../../files/domains/top-1m-domains.csv'
        )
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:  # Format: rank,domain
                        top_domains.add(row[1].lower())
            print(f"Loaded {len(top_domains)} top domains")
        except Exception as e:
            print(f"Warning: Could not load top domains file: {e}")
        
        return top_domains

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
                            hostname = hostname.lower()
                            # Skip if domain is in top 1M list
                            if hostname in self.top_domains:
                                print(f"Skipping top domain: {hostname}")
                                continue
                            addresses.append(hostname)
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
