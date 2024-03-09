import json

def read_existing_data():
    data = {}
    with open("data.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            (key, value) = line.split(":", 1)
            data[key] = json.loads(value)
    return data

def read_cities():
    with open("cities.txt", "r") as f:
        lines = f.readlines()
        return [l.strip() for l in lines]

