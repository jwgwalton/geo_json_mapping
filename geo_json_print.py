import geojson
import json
import csv
import matplotlib as mpl
import matplotlib.cm as cm
import copy as cp

STATISTICS_FILE_LOCATION = "statistics/gva_values.csv"
NUTS_REGIONS_FILE = "geojson/NUTS_UK.geojson"
OUTPUT_NUTS_REGIONS_WITH_STATS = 'geojson/NUTS_UK_GVA.geojson'
STATISTIC_NAME = 'GVA in Millions'

def read_csv(file_location):
    statistical_values = {}
    with open(file_location) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            statistical_values[row[0]]=row[1]
    return statistical_values


def normalise_values(values):
    max_value = max([int(i) for i in values.values()])
    min_value = min([int(i) for i in values.values()])
    #print('max_gva_value', max_value)
    #print('min_gva_value', min_value)
    for value in values:
        #print('nut_code', nut_gva_value)
        #print('gva_value', nut_gva_values[nut_gva_value])
        values[value]= (int(values[value])  - min_value)/(max_value - min_value)
    return values

def generate_colour(statistic_value):
    #TODO:  MAPPING FROM NORMALISED NUMBERS TO HEXADECIMAL COLOURS
    return_colour = "green"
    if statistic_value > 0.2:
        return_colour = "red"
    if 0.2 > statistic_value > 0.01:
        return_colour = "blue"
    print('return_colour', return_colour)
    return (0,255*(1-statistic_value), 255*statistic_value)

def gather_statistic(statistic_values, geojson):
    nuts_code = geojson.properties["NUTS312CD"]
    return statistic_values.get(nuts_code, 0) # retrieve gva value, sensible default of 0 if not found


# open geojson file
with open(NUTS_REGIONS_FILE) as json_file:
    geo_json_data = geojson.load(json_file)

# READ IN STATISTICS & NORMALISE
unnormalised_values = read_csv(STATISTICS_FILE_LOCATION)
normalised_values = normalise_values(cp.copy(unnormalised_values))


# update colour based off statistic and append statistic as property
for feature in geo_json_data.features:
    normalised_value = gather_statistic(normalised_values, feature)
    unnormalised_value = gather_statistic(unnormalised_values, feature)
    feature.properties["fill"] = generate_colour(normalised_value)
    feature.properties[STATISTIC_NAME] = unnormalised_value

# SAVE FILE TO OUTPUT
with open(OUTPUT_NUTS_REGIONS_WITH_STATS, 'w') as output_json_file:
    json.dump(geo_json_data, output_json_file)
