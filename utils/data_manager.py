import csv
import os

FILE = "data.csv" 

def load_data():
    if not os.path.exists(FILE):
        return []

    with open(FILE, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_data(data):
    if not data:
        return

    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)