from geojson_mapper import GeoJsonMapper

STATISTICS_FOLDER = "statistics/"
GEOJSON_FOLDER = "geojson/"

STATISTICS_FILE_LOCATION = STATISTICS_FOLDER+"modelled_nuts1_gva_values.csv"
NUTS_REGIONS_FILE = GEOJSON_FOLDER+"NUTS1_EU.geojson"
OUTPUT_NUTS_REGIONS_WITH_STATS = GEOJSON_FOLDER+'MODELLED_NUTS1_EU_GVA_with_mapper.geojson'

STATISTIC_NAME = 'GVA in Thousands'

REGION_TYPE = "NUTS_ID"

mapper = GeoJsonMapper(STATISTIC_NAME)

mapper.label_geojson(NUTS_REGIONS_FILE, STATISTICS_FILE_LOCATION, region_identifier=REGION_TYPE)

mapper.print_geo_json(OUTPUT_NUTS_REGIONS_WITH_STATS)
