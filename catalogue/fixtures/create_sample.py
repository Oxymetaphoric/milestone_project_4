import csv
from pathlib import Path

def create_sample_csv_streaming(source_csv, sample_csv, num_lines=500):
    """
    Create a sample CSV from a large file without loading it all into memory.
    Takes the first num_lines + 1 (including header) from the source file.
    
    Args:
        source_csv (str): Path to your original CSV file
        sample_csv (str): Path where to save the sample CSV
        num_lines (int): Number of data rows to include in sample (default: 5)
    """
    with open(source_csv, 'r', encoding='utf-8') as source:
        # Read and write the header
        header = next(csv.reader(source))
        
        with open(sample_csv, 'w', encoding='utf-8', newline='') as target:
            writer = csv.writer(target)
            writer.writerow(header)
            
            # Get the next num_lines rows
            for _ in range(num_lines):
                try:
                    row = next(csv.reader(source))
                    writer.writerow(row)
                except StopIteration:
                    break

if __name__ == "__main__":
    # Replace these with your actual file paths
    SOURCE_CSV = "./catalogue/fixtures/stock-items.csv"
    SAMPLE_CSV = "./catalogue/fixtures/sample_dataset.csv"
    
    source_size = Path(SOURCE_CSV).stat().st_size / (1024 * 1024 * 1024)  # Size in GB
    print(f"Source file size: {source_size:.2f} GB")
    
    create_sample_csv_streaming(SOURCE_CSV, SAMPLE_CSV)
    print(f"Created sample CSV with first x data rows at: {SAMPLE_CSV}")
