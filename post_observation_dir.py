#!/usr/bin/python3

from pyinaturalist.rest_api import create_observations
from pyinaturalist.rest_api import add_photo_to_observation
from pyinaturalist.rest_api import get_access_token
from PIL import Image
from PIL import ExifTags
import os
import re
import base64
import argparse
import getpass
import datetime


# Arguments
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-a', '--app_id',  help='Specify iNaturalist Application ID',required=True)
parser.add_argument('-s', '--app_secret', help='Specify iNaturalist Application Secret',required=True)
parser.add_argument('-u', '--username', help='Specify iNaturalist username',required=True)
parser.add_argument('-p', '--password', help='Specify iNaturalist password')
parser.add_argument('-d', '--directory', help='Specify Directory path',required=True)
parser.add_argument('-t', '--taxon_id', help='Specify Taxon id')
parser.add_argument('-tz', '--time_zone', help='Specify Time Zone', default="Asia/Kolkata")
parser.add_argument('-la', '--latitude', help='Specify Latitude')
parser.add_argument('-lo', '--longitude', help='Specify Longitude')
args = parser.parse_args()

if not args.password: 
    args.password = getpass.getpass()

# Date from Image
def get_date(image):
    # Gets all the exif data from the photo
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in ExifTags.TAGS
        
    }
    # Pulls the date and time from the exif format
    date = exif.get('DateTime').split()[0]
    time = exif.get('DateTime').split()[1]
    # Reformats the date to use - instead of : 
    for character in date:
        if character == ':':
            date = date.replace(character, '-')
    # Combines the date and time to match the format pyinaturalist wants, 
    date_time = str(date) + 'T' + str(time)
    # returns a date and time formatted to submit to iNaturalist with
    # pyinaturalist
    return date_time
    
def get_lat_long(image):
    # Gets all the exif data from the photo
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in image._getexif().items()
        if k in ExifTags.TAGS
    }
    # From all the exif data, pulls the GPS data
    gps_info = exif.get('GPSInfo')
    # The GPS data is in a odd format, so have to dig for it a bit. This was
    # only tested on files lightroom tagged. 
    latitude_direction = str(gps_info.get(1)[0])
    latitude_degrees = float(gps_info.get(2)[0][0])
    minutes = float(gps_info.get(2)[1][0])
    multiplier = float(gps_info.get(2)[1][1])
    latitude_minutes = minutes/multiplier
    
    # The sign is changed depending on if this is N or S
    if latitude_direction == 'N' or latitude_direction == 'n':
        latitude = latitude_degrees+latitude_minutes/60
    elif latitude_direction == 'S' or latitude_direction == 's':
        latitude = -(latitude_degrees+latitude_minutes/60)
        
    longitude_direction = gps_info.get(3)[0]
    longitude_degrees = gps_info.get(4)[0][0]
    minutes = float(gps_info.get(4)[1][0])
    multiplier = float(gps_info.get(4)[1][1])
    longitude_minutes = minutes/multiplier
    # The sign is changed depending on if this is E or W
    if longitude_direction == 'E' or longitude_direction == 'e':
        longitude = longitude_degrees+longitude_minutes/60
    elif longitude_direction == 'W' or longitude_direction == 'w':
        longitude = -(longitude_degrees+longitude_minutes/60)
    
    latitude_longitude = [latitude, longitude]
    
    # Returns a list with both latitude and longiude in decimal format.
    return latitude_longitude


directory_in_str = args.directory
directory = os.fsencode(directory_in_str)
user = args.username
passw = args.password
app = args.app_id
secret = args.app_secret

print('Uploading all photos in directory contained in ' + directory_in_str+' as individual observations' )

for file in os.walk(directory):
    if file[0] == directory:
        files = file

file_paths = []
for file in files[2]:   # All files are in files[2]
    file_path = files[0] + file  # files[0] has the path to the folder
    file_paths.append(file_path) # Makes a big list of paths
    
for bfile in file_paths:
    file = bfile.decode('utf-8')
    print (file)
    img = Image.open(file)
    
    try:
        img_exif = img._getexif()
    except:
        print("Warning: No exif value in the image. Will user current date and speciied coordinates")
        date_time = datetime.datetime.now().isoformat()
        latitude_longitude = [args.latitude, args.longitude]
    
    if img_exif:
        try:
            date_time = get_date(img)
        except:
            print ("Warning: No date value in the image. Using current date")
            date_time = datetime.datetime.now().isoformat()
        try:
            latitude_longitude = get_lat_long(img)
        except:
            print ("Warning: No Lat Long values in the image. If any coordinates are specified, they will be used")
            latitude_longitude = [args.latitude, args.longitude]
    else:
        print("Warning: No exif value in the image. Will user current date and speciied coordinates")
        date_time = datetime.datetime.now().isoformat()
        latitude_longitude = [args.latitude, args.longitude]
    
    
    print(latitude_longitude)
    
    params = {'observation':
             {'taxon_id': args.taxon_id,
              'observed_on_string': date_time,
              'time_zone': args.time_zone,
              'description': '',
              'tag_list': '',
              'latitude': latitude_longitude[0],
              'longitude': latitude_longitude[1],
              'positional_accuracy': 50, # meters,
              'observation_field_values_attributes':
                 [{'observation_field_id': '','value': ''}],
              },}
              # This is getting a token to allow photos to be uploaded.
    token = get_access_token(username=user, password=passw,
                         app_id=app,
                         app_secret=secret)
    r = create_observations(params=params, access_token=token)
    new_observation_id = r[0]['id']
    add_photo_to_observation(observation_id=new_observation_id, file_object=open(file,'rb'), access_token=token)
