from typing import Dict, List

class SuietLoader:
    def extract_address_by_type(self, data: List[List[str]], type_: str) -> List[str]:
        # Filter rows: must have at least 5 columns and status must be 'scam'
        filtered_data = [row for row in data if len(row) >= 5 and row[0] == 'scam']
        addresses = []

        for row in filtered_data:
            if row[2] == type_:  # Check type column
                object_id = row[4].strip()  # Get and clean ObjectType column
                if object_id:  # Only add non-empty addresses
                    addresses.append(object_id)
        return addresses

    def process_sheet_data(self, spreadsheet_data: List[List[str]]) -> Dict[str, List[str]]:
        return {
            'coin': self.extract_address_by_type(spreadsheet_data, 'Coin'),
            'object': self.extract_address_by_type(spreadsheet_data, 'NFT') +
                     self.extract_address_by_type(spreadsheet_data, 'Object'),
            'package': self.extract_address_by_type(spreadsheet_data, 'Package'),
        }
