import geojson
import json
import csv

from colour_mapper import RGBColourMapper


class GeoJsonMapper:

    def __init__(self, label_name, colour_mapper_type='inferno'):
        self.geojson = None
        self.label_name = label_name
        self.rgb_colour_mapper = RGBColourMapper(colour_mapper_type)

    def _read_csv(self, file_location):
        enrichment_data = {}
        with open(file_location) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                enrichment_data[row[0]] = row[1]
        return enrichment_data

    def _open_geojson(self, file_path):
        with open(file_path) as geojson_file:
            self.geojson = geojson.load(geojson_file)

    def _normalise_values(self, values):
        max_value = max([int(i) for i in values.values()])
        min_value = min([int(i) for i in values.values()])
        for value in values:
            values[value] = (int(values[value]) - min_value)/(max_value - min_value)
        return values

    def _get_value_for_region(self, region_map, region, region_identifier_type):
        region_name = region.properties[region_identifier_type]
        return region_map.get(region_name, 0)

    def label_geojson(self, geojson_file_path, labels_file_path, region_identifier):
        # update colour based off statistic and append statistic as property
        self._open_geojson(geojson_file_path)
        unnormalised_values = self._read_csv(labels_file_path)
        normalised_values = self._normalise_values(unnormalised_values.copy())
        for region in self.geojson.features:
            normalised_value = self._get_value_for_region(normalised_values, region, region_identifier)
            unnormalised_value = self._get_value_for_region(unnormalised_values, region, region_identifier)
            self._update_region_colour_and_label(region, normalised_value, unnormalised_value)

    def _update_region_colour_and_label(self, feature, normalised_value, unnormalised_value):
        feature.properties["fill"] = self.rgb_colour_mapper.generate_hex_colour(normalised_value)
        feature.properties[self.label_name] = unnormalised_value

    def print_geo_json(self, output_file_path):
        with open(output_file_path, 'w+') as output_json_file:
            json.dump(self.geojson, output_json_file)


