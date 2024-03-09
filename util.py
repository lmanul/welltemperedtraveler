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

def write_out(master_data, data_file):
    serialized = ""
    for location in sorted(master_data.keys()):
        serialized += location + ":" + json.dumps(master_data[location], sort_keys=True) + "\n"
        with open(data_file, "w") as f:
            f.write(serialized)
