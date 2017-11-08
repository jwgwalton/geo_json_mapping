import geojson
import json

GVA_VALUES = [{ "UKC11": 1000}, {"UKC12": 1001}]

def assign_gva_values(gva_values, geojson):
    for value in gva_values:
        print('value', value)

# open geojson file
with open("data/NUTS_UK.geojson") as json_file:
    geo_json_data = geojson.load(json_file)

# update colour based off caluclated statistics
# TODO: ACTUALLY PULL STATISTICS AND THEN MAP TO A COLOUR
for feature in geo_json_data.features:
    #print(feature)
    feature.properties["fill"] = "red"

# SAVE FILE TO OUTPUT
with open('data/NUTS_UK_GVA.geojson', 'w') as output_json_file:
    json.dump(geo_json_data, output_json_file)



#assign_gva_values(GVA_VALUES, geo_json_data)
