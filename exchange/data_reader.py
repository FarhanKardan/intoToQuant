import pandas as pd
from pathlib import Path
from datetime import datetime
import re

# Handle import for both direct execution and module import
try:
    from .models import TickData
except ImportError:
    from models import TickData

class DataReader:
    def __init__(self, data_dir="data"):
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        # Go up one level to the project root and then to data directory
        self.data_dir = script_dir.parent / data_dir
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def read_csv(self, filename):
        file_path = self.data_dir / filename
        if file_path.exists():
            return pd.read_csv(file_path)
        else:
            print(f"File {filename} not found in {self.data_dir}")
            return None
    
    def get_files_by_date_range(self, start_date, end_date, file_pattern="*"):
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        matching_files = []
        
        for file in self.data_dir.glob(file_pattern):
            if file.is_file():
                date_match = re.search(r'(\d{4}[-_]\d{2}[-_]\d{2})', file.name)
                if date_match:
                    file_date_str = date_match.group(1).replace('_', '-')
                    file_date = pd.to_datetime(file_date_str)
                    
                    if start_dt <= file_date <= end_dt:
                        matching_files.append(file.name)
        
        return sorted(matching_files)
    
    def read_csv_by_date_range(self, start_date, end_date, file_pattern="*", aggregate=True):
        files = self.get_files_by_date_range(start_date, end_date, file_pattern)
        
        if not files:
            print(f"No files found in date range {start_date} to {end_date}")
            return None
        
        dataframes = []
        for filename in files:
            df = self.read_csv(filename)
            if df is not None:
                dataframes.append(df)
        
        if not dataframes:
            return None
        
        if aggregate:
            return pd.concat(dataframes, ignore_index=True)
        else:
            return dataframes
    
    def iterate_records(self, start_date, end_date, file_pattern="*.csv"):
        files = self.get_files_by_date_range(start_date, end_date, file_pattern)
        
        if not files:
            print(f"No files found in date range {start_date} to {end_date}")
            return
        
        for filename in files:
            df = self.read_csv(filename)
            if df is not None:
                for index, record in df.iterrows():
                    # Convert record to TickData model
                    try:
                        # Extract symbol from filename (e.g., "BTCUSDT_2024-05-01.csv" -> "BTCUSDT")
                        symbol = filename.split('_')[0]
                        
                        # Convert timestamp from milliseconds to datetime
                        timestamp_ms = record.get('timestamp', 0)
                        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                        
                        tick_data = TickData(
                            symbol=symbol,
                            side=str(record.get('side', '')),
                            size=float(record.get('volume', 0)),
                            price=float(record.get('price', 0)),
                            timestamp=timestamp
                        )
                        
                        yield {
                            'filename': filename,
                            'index': index,
                            'tick_data': tick_data
                        }
                    except (ValueError, TypeError) as e:
                        print(f"Error converting record at index {index} in {filename}: {e}")
                        continue


# Use
def main():
    # Initialize data reader
    data_reader = DataReader()
    
    # Read CSV data by date range
    start_date = "2024-05-01"
    end_date = "2024-05-07"
    
    # Get files in date range
    files = data_reader.get_files_by_date_range(start_date, end_date, "*.csv")
    print(f"Files found in date range {start_date} to {end_date}:", files)
    
    # Read and aggregate data
    aggregated_data = data_reader.read_csv_by_date_range(start_date, end_date, "*.csv", aggregate=True)
    if aggregated_data is not None:
        print(f"Aggregated data shape: {aggregated_data.shape}")
        print("First few rows:", aggregated_data.head())
    
    # Iterate over records
    print("\nIterating over records:")
    record_count = 0
    for record_info in data_reader.iterate_records(start_date, end_date, "*.csv"):
        record_count += 1
        print(f"Record {record_count}: File={record_info['filename']}, Index={record_info['index']}")
        print(f"Data: {record_info['tick_data']}")
        
        # Limit to first 3 records for demonstration
        if record_count >= 3:
            break

if __name__ == "__main__":
    main() 