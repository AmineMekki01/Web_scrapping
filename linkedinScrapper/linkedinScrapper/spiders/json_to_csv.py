import json
import csv
def to_csv(filename):
    with open(filename + '.json', 'r') as json_file:
        data = json.load(json_file)

    with open(filename+'.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(data[0].keys())

        for row in data:
            writer.writerow(row.values())
            
# to_csv("jobs")