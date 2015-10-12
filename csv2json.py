import csv
import json

csvfile = open('servers.csv', 'r')
jsonfile = open('servers.json', 'w')

fieldnames = ("server","port","type")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')