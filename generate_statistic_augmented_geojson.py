import geojson
import json
import csv
import matplotlib.cm as cm
import matplotlib.colors as colors
import copy as cp

STATISTICS_FILE_LOCATION = "statistics/nuts3_gva_values.csv"
NUTS_REGIONS_FILE = "geojson/NUTS3_UK.geojson"
OUTPUT_NUTS_REGIONS_WITH_STATS = 'geojson/NUTS3_UK_GVA.geojson'
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
    for value in values:
        values[value]= (int(values[value])  - min_value)/(max_value - min_value)
    return values


def gather_statistic(statistic_values, geojson):
    nuts_code = geojson.properties["NUTS312CD"]
    return statistic_values.get(nuts_code, 0) # retrieve gva value, sensible default of 0 if not found


# OPEN GEOJSON FILE OF NUT3 REGIONS
with open(NUTS_REGIONS_FILE) as json_file:
    geo_json_data = geojson.load(json_file)

# READ IN CSV OF STATISTICS FOR NUT3 REGIONS
unnormalised_values = read_csv(STATISTICS_FILE_LOCATION)
normalised_values = normalise_values(cp.copy(unnormalised_values))

normalised_max =1
normalised_min = 0
norm = colors.Normalize(vmin=normalised_min, vmax=normalised_max)
rgb_colour_mapper = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap('RdYlGn'))

def generate_hex_colour(colour_mapper, value):
    rgb = colour_mapper.to_rgba(value)[:3]
    return '#%02x%02x%02x' % tuple([int(255*colour) for colour in rgb])

# update colour based off statistic and append statistic as property
for feature in geo_json_data.features:
    normalised_value = gather_statistic(normalised_values, feature)
    unnormalised_value = gather_statistic(unnormalised_values, feature)
    feature.properties["fill"] = generate_hex_colour(rgb_colour_mapper, normalised_value)
    feature.properties[STATISTIC_NAME] = unnormalised_value

# SAVE FILE TO OUTPUT FILE
with open(OUTPUT_NUTS_REGIONS_WITH_STATS, 'w') as output_json_file:
    json.dump(geo_json_data, output_json_file)
