import geojson
import json
import csv

def read_gva_csv(file_location):
    gva_values = {}
    with open(file_location) as gva_values_csv:
        csv_reader = csv.reader(gva_values_csv)
        for row in csv_reader:
            gva_values[row[0]]=row[1]
    return gva_values

def map_value_to_colour(value):
    #TODO: NORMALISE THE NUMBERS AND BIN THE VALUES TO THEN ASSIGN COLOURS BASED OFF BIN VALUES
    if value > 1:
        return "blue"
    else:
        return "red"

def map_gva_to_colour(gva_values, geojson):
    nuts_code = geojson.properties["NUTS312CD"]
    print('nuts_code: ', nuts_code)
    gva_value = gva_values.get(nuts_code, 0) # retrieve gva value
    print('gva_value: ', gva_value)
    return map_value_to_colour(int(gva_value))

# open geojson file
with open("data/NUTS_UK.geojson") as json_file:
    geo_json_data = geojson.load(json_file)

# READ IN STATISTICS
gva_values = read_gva_csv("data/gva_values.csv")

# update colour based off caluclated statistics
for feature in geo_json_data.features:
    feature.properties["fill"] = map_gva_to_colour(gva_values, feature)


# SAVE FILE TO OUTPUT
with open('data/NUTS_UK_GVA.geojson', 'w') as output_json_file:
    json.dump(geo_json_data, output_json_file)



#assign_gva_values(GVA_VALUES, geo_json_data)
