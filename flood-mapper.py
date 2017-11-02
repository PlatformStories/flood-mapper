import json
import os
import protogen
from osgeo import gdal

input_ports_location = '/mnt/work/input/'
output_ports_location = '/mnt/work/output/'

# Get image directory
image_dir = os.path.join(input_ports_location, 'image')

# Point to image file. If there are multiple tif's in multiple subdirectories, pick one.
image = [os.path.join(dp, f) for dp, dn, fn in os.walk(image_dir) for f in fn if ('tif' in f) or ('TIF' in f)][0]

# Count bands
no_bands = gdal.Open(image).RasterCount

# Read from ports.json
input_ports_path = os.path.join(input_ports_location, 'ports.json')
if os.path.exists(input_ports_path):
    string_ports = json.load(open(input_ports_path))
else:
    string_ports = None

if string_ports:
    tolerance = float(string_ports.get('tolerance', '50'))
    min_size = float(string_ports.get('min_size', '1000'))
    min_width = float(string_ports.get('min_width', '10'))
    confidence = float(string_ports.get('confidence', '1'))
else:
    tolerance = 50.0
    min_size = 1000.0
    min_width = 10.0
    confidence = 1.0

# Create output directory
output_dir = os.path.join(output_ports_location, 'image')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
os.chdir(output_dir)

# Run flood mapper protocol
p = protogen.Interface('crime', 'flood_water_mapper')
p.crime.flood_water_mapper.tolerance = tolerance
p.crime.flood_water_mapper.moisture = confidence
p.crime.flood_water_mapper.min_size = min_size
p.crime.flood_water_mapper.min_width = min_width
p.crime.flood_water_mapper.binary_output = True
p.image = image
p.image_config.bands = range(1, no_bands+1)

p.execute()
