import csv
import json
import os

data_path = 'temples_to_add.json'
csv_path = r'datasets\AP_DATASET.CSV'

if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit(1)

with open(data_path, 'r', encoding='utf-8') as f:
    new_temples = json.load(f)

with open(csv_path, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(new_temples)

print(f"Successfully added {len(new_temples)} temples to {csv_path}")
