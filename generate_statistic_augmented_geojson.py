import geojson
import json
import csv
import matplotlib.cm as cm
import matplotlib.colors as colors
import copy as cp

STATISTICS_FILE_LOCATION = "statistics/gva_values.csv"
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

def generate_colour(statistic_value):
    #TODO:  MAPPING FROM NORMALISED NUMBERS TO HEXADECIMAL COLOURS
    colour_value = 255*statistic_value*10
    print('colour_value', colour_value)
    #return 'rgb(0,'+str(255*(1-statistic_value))+', ' + str(255*statistic_value)+')'
    return 'rgb(0,0, ' + str(colour_value)+')'
    #return (0, 255*(1-statistic_value), 255*statistic_value)

def gather_statistic(statistic_values, geojson):
    nuts_code = geojson.properties["NUTS312CD"]
    return statistic_values.get(nuts_code, 0) # retrieve gva value, sensible default of 0 if not found


# OPEN GEOJSON FILE OF NUT3 REGIONS
with open(NUTS_REGIONS_FILE) as json_file:
    geo_json_data = geojson.load(json_file)

# READ IN CSV OF STATISTICS FOR NUT3 REGIONS
unnormalised_values = read_csv(STATISTICS_FILE_LOCATION)
normalised_values = normalise_values(cp.copy(unnormalised_values))

# create colou map
max_value = max([int(i) for i in unnormalised_values.values()])
min_value = min([int(i) for i in unnormalised_values.values()])

#FUNCTION FOR
#norm = colors.Normalize(vmin=min_value, vmax=max_value)
#print("norm: ", norm)
#to_rgb = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap('RdYlGn'))



#statistic_values = [int(i) for i in unnormalised_values.values()]
#colour_values = to_rgb.to_rgba(statistic_values)[:3]
#print('colour_values: ', colour_values)
#colour_encoded_regions

norm = colors.Normalize(vmin=0, vmax=1)
f2rgb = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap('RdYlGn'))

def f2hex(f2rgb, f):
    rgb = f2rgb.to_rgba(f)[:3]
    print('rgb: ', rgb)
    return rgb #tuple([255*fc for fc in rgb])

# update colour based off statistic and append statistic as property
for feature in geo_json_data.features:
    normalised_value = gather_statistic(normalised_values, feature)
    unnormalised_value = gather_statistic(unnormalised_values, feature)
    colour_value = f2hex(f2rgb, normalised_value)
    print('colour_value: ', colour_value)
    feature.properties["fill"] = "rgb"+str(colour_value)+")"
    feature.properties[STATISTIC_NAME] = unnormalised_value

# SAVE FILE TO OUTPUT FILE
with open(OUTPUT_NUTS_REGIONS_WITH_STATS, 'w') as output_json_file:
    json.dump(geo_json_data, output_json_file)
