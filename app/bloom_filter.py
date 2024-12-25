import os
import json
from probables import BloomFilter

DIST_DIR = "./dist"
ERROR_RATE = 0.001  # Adjust error rate as needed

def create_bloom_filter(blocklist, error_rate=0.001):
    """
    Create a BloomFilter given the blocklist and return the instance.
    """
    # Initialize BloomFilter with estimated elements and error rate
    bf = BloomFilter(est_elements=len(blocklist), false_positive_rate=error_rate)
    
    # Add each item to the bloom filter
    for item in blocklist:
        bf.add(item)
    return bf

def bloom_filter_to_json(bf: BloomFilter, filename: str):
    """
    Convert a BloomFilter to a JSON-serializable structure.
    """
    bf.export(filename.replace('.json', '.blm'))
    return {
        "file": filename.split('/')[-1].replace('.json', '.blm'),
        "est_elements": bf.estimated_elements,
        "false_positive_rate": bf.false_positive_rate,
        "number_bits": bf.number_bits,
        "number_hashes": bf.number_hashes,
    }

def process_file(filename):
    """
    Read the given JSON file, extract the blocklist, generate a bloom filter,
    then save to a new *-bloom.json file.
    """
    filepath = os.path.join(DIST_DIR, filename)
    # Read original JSON file
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract blocklist and generate bloom filter
    blocklist = data.get("blocklist", [])
    bf = create_bloom_filter(blocklist, ERROR_RATE)

    # Serialize bloom filter to JSON
    bf_json = bloom_filter_to_json(bf, os.path.join(DIST_DIR, filename))

    # Output filename, e.g., coin-list-bloom.json
    base_name, ext = os.path.splitext(filename)
    out_filename = f"{base_name}.bloom.json"
    out_filepath = os.path.join(DIST_DIR, out_filename)

    # Write new JSON file
    with open(out_filepath, 'w', encoding='utf-8') as f:
        json.dump(bf_json, f, ensure_ascii=False, indent=2)

    print(f"Processed {filename} -> {out_filename}")

def main():
    """
    Main function: Process the 4 target files in dist directory.
    """
    target_files = [
        "coin-list.json",
        "domain-list.json",
        "object-list.json",
        "package-list.json"
    ]
    
    for tf in target_files:
        process_file(tf)

if __name__ == "__main__":
    main()