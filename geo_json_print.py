import geojson

with open("data/NUTS_UK.geojson") as json_file:
    json_data = geojson.load(json_file)

print(json_data.keys())
