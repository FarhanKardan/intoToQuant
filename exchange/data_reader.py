import pandas as pd
from pathlib import Path
from datetime import datetime
import re

from exchange.models import TickData

class DataReader:
    def __init__(self, data_dir="data"):
        script_dir = Path(__file__).parent
        self.data_dir = script_dir.parent / data_dir
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def read_csv(self, filename):
        file_path = self.data_dir / filename
        return pd.read_csv(file_path) if file_path.exists() else None
    
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
            return None
        
        dataframes = [self.read_csv(filename) for filename in files]
        dataframes = [df for df in dataframes if df is not None]
        
        if not dataframes:
            return None
        
        return pd.concat(dataframes, ignore_index=True) if aggregate else dataframes
    
    def iterate_records(self, start_date, end_date, file_pattern="*.csv"):
        files = self.get_files_by_date_range(start_date, end_date, file_pattern)
        if not files:
            return
        
        for filename in files:
            df = self.read_csv(filename)
            if df is not None:
                for index, record in df.iterrows():
                    try:
                        symbol = filename.split('_')[0]
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
                    except (ValueError, TypeError):
                        continue

def main():
    data_reader = DataReader()
    start_date = "2024-05-01"
    end_date = "2024-05-07"
    
    files = data_reader.get_files_by_date_range(start_date, end_date, "*.csv")
    print(f"Files: {files}")
    
    aggregated_data = data_reader.read_csv_by_date_range(start_date, end_date, "*.csv", aggregate=True)
    if aggregated_data is not None:
        print(f"Data shape: {aggregated_data.shape}")
        print("Sample:", aggregated_data.head())

if __name__ == "__main__":
    main() 