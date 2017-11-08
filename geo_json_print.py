import geojson
import json
import csv
import numpy as np

def read_gva_csv(file_location):
    nut_gva_values = {}
    with open(file_location) as gva_values_csv:
        csv_reader = csv.reader(gva_values_csv)
        for row in csv_reader:
            nut_gva_values[row[0]]=row[1]
    print(nut_gva_values)
    normalised_gva_values = normalise_gva_values(nut_gva_values)
    print(normalised_gva_values)
    return normalised_gva_values #map_gva_to_colour(gva_values) # THINK HOW TO


def normalise_gva_values(nut_gva_values):
    max_value = max([int(i) for i in nut_gva_values.values()])
    min_value = min([int(i) for i in nut_gva_values.values()])
    print('max_gva_value', max_value)
    print('min_gva_value', min_value)
    for nut_gva_value in nut_gva_values:
        print('nut_code', nut_gva_value)
        print('gva_value', nut_gva_values[nut_gva_value])
        nut_gva_values[nut_gva_value]= (int(nut_gva_values[nut_gva_value])  - min_value)/(max_value - min_value)
    return nut_gva_values

def map_value_to_colour(value):
    #TODO: NORMALISE THE NUMBERS AND BIN THE VALUES TO THEN ASSIGN COLOURS BASED OFF BIN VALUES

    if value > 0.7:
        return "red"
    if value > 0.4:
        return 'green'
    else:
        return "blue"

def map_gva_to_colour(gva_values, geojson):
    nuts_code = geojson.properties["NUTS312CD"]
    #print('nuts_code: ', nuts_code)
    gva_value = gva_values.get(nuts_code, 0) # retrieve gva value, sensible default of 0 if not found
    #print('gva_value: ', gva_value)
    return map_value_to_colour(int(gva_value))

# open geojson file
with open("geojson/NUTS_UK.geojson") as json_file:
    geo_json_data = geojson.load(json_file)

# READ IN STATISTICS
gva_values = read_gva_csv("statistics/gva_values.csv")

# update colour based off caluclated statistics
for feature in geo_json_data.features:
    feature.properties["fill"] = map_gva_to_colour(gva_values, feature)


# SAVE FILE TO OUTPUT
with open('geojson/NUTS_UK_GVA.geojson', 'w') as output_json_file:
    json.dump(geo_json_data, output_json_file)
