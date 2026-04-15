"""
Task 1: Dataset Generator
Generates a synthetic weather_data.csv with daily temperature records.
Values are random floats between -30 and 50 (Celsius).
No built-in min/max/sort used.
"""

import random
import os


class WeatherLoader:
    """Handles CSV generation and loading of temperature data."""

    def __init__(self, filepath="weather_data.csv"):
        self.filepath = filepath

    def generate_csv(self, num_records=5000, seed=42):
        """Generate a synthetic CSV file with daily temperature records."""
        random.seed(seed)

        with open(self.filepath, "w") as f:
            f.write("id,date,temperature_celsius\n")
            for i in range(1, num_records + 1):
                year  = 2010 + (i // 365)
                month = ((i - 1) % 12) + 1
                day   = ((i - 1) % 28) + 1
                date  = f"{year}-{month:02d}-{day:02d}"
                temp  = round(random.uniform(-30.0, 50.0), 2)
                f.write(f"{i},{date},{temp}\n")

        print(f"[DataGen] Generated {num_records} records -> '{self.filepath}'")

    def load_csv(self):
        """
        Read the CSV and return a plain Python list of temperature floats.
        No built-ins like min/max/sort are used on the data.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(
                f"'{self.filepath}' not found. Run generate_csv() first."
            )

        temperatures = []
        with open(self.filepath, "r") as f:
            header = True
            for line in f:
                if header:
                    header = False
                    continue
                parts = line.strip().split(",")
                if len(parts) == 3:
                    temperatures.append(float(parts[2]))

        print(f"[DataGen] Loaded {len(temperatures)} temperature records.")
        return temperatures


#  quick self-test 
if __name__ == "__main__":
    loader = WeatherLoader()
    loader.generate_csv(5000)
    data = loader.load_csv()
    print(f"[DataGen] First 5 values : {data[:5]}")
    print(f"[DataGen] Last  5 values : {data[-5:]}")
