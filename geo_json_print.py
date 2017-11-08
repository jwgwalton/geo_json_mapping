import geojson
import json
import csv
import matplotlib as mpl
import matplotlib.cm as cm

STATISTICS_FILE_LOCATION = "statistics/gva_values.csv"
NUTS_REGIONS_FILE = "geojson/NUTS_UK.geojson"
OUTPUT_NUTS_REGIONS_WITH_STATS = 'geojson/NUTS_UK_GVA.geojson'

def read_gva_csv(file_location):
    nut_gva_values = {}
    with open(file_location) as gva_values_csv:
        csv_reader = csv.reader(gva_values_csv)
        for row in csv_reader:
            nut_gva_values[row[0]]=row[1]
    return normalise_gva_values(nut_gva_values)


def normalise_gva_values(nut_gva_values):
    max_value = max([int(i) for i in nut_gva_values.values()])
    min_value = min([int(i) for i in nut_gva_values.values()])
    #print('max_gva_value', max_value)
    #print('min_gva_value', min_value)
    for nut_gva_value in nut_gva_values:
        #print('nut_code', nut_gva_value)
        #print('gva_value', nut_gva_values[nut_gva_value])
        nut_gva_values[nut_gva_value]= (int(nut_gva_values[nut_gva_value])  - min_value)/(max_value - min_value)
    return nut_gva_values

def generate_colour(gva_value):
    #TODO:  MAPPING FROM NORMALISED NUMBERS TO HEXADECIMAL COLOURS
    return_colour = "green"
    if gva_value > 0.2:
        return_colour = "red"
    if 0.2 > gva_value > 0.01:
        return_colour = "blue"
    print('return_colour', return_colour)
    return return_colour

def map_gva_to_colour(gva_values, geojson):
    nuts_code = geojson.properties["NUTS312CD"]
    #print('nuts_code: ', nuts_code)
    gva_value = gva_values.get(nuts_code, 0) # retrieve gva value, sensible default of 0 if not found
    print('gva_value: ', gva_value)
    return generate_colour(gva_value)

def gather_raw_statistic(gva_values, geojson):
    nuts_code = geojson.properties["NUTS312CD"]
    return gva_values.get(nuts_code, 0) # retrieve gva value, sensible default of 0 if not found


# open geojson file
with open(NUTS_REGIONS_FILE) as json_file:
    geo_json_data = geojson.load(json_file)

# READ IN STATISTICS
gva_values = read_gva_csv(STATISTICS_FILE_LOCATION)

# update colour based off caluclated statistics
for feature in geo_json_data.features:
    gva_value = gather_raw_statistic(gva_values, feature)
    feature.properties["fill"] = generate_colour(gva_value)
    feature.properties['GVA'] = gva_value

# SAVE FILE TO OUTPUT
with open(OUTPUT_NUTS_REGIONS_WITH_STATS, 'w') as output_json_file:
    json.dump(geo_json_data, output_json_file)
