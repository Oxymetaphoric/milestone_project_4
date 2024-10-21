import csv
import sys

def get_csv_headers(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 stripHeaders.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    headers = get_csv_headers(csv_file)
    
    # Print headers to stdout (which can be redirected to a file)
    for header in headers:
        print(header)
