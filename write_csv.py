import csv

def write_dict(csv_path, data_dict):
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='|')
        # rows = zip(*data_dict.values())
        writer.writerows(data_dict)