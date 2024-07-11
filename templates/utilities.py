import csv
import json

def write_to_csv(filename, data):
    keys = data[0].keys() if data else []
    with open(f'{filename}.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def update_json(filename, data):
    with open(f'{filename}.json', 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=4)
