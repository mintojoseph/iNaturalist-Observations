
# iNaturalist-Observations

Batch uploads using pyinaturalist.

Based on the code from [glmory](https://github.com/glmory/iNaturalist-Uploads/blob/master/upload_folder.py).

The program would upload each photo as induvidual obesrvation from the specified directory.

## Requirements

* Create app id and secret [from inaturalist](https://www.inaturalist.org/oauth/applications/new)
* Directory with photos from one general taxon id. For example, 3 for Birds.

## Parameters

``` python3
$ python3 post_observation_dir.py -h
usage: post_observation_dir.py [-h] -a APP_ID -s APP_SECRET -u USERNAME
                               [-p PASSWORD] -d DIRECTORY [-t TAXON_ID]
                               [-tz TIME_ZONE] [-la LATITUDE] [-lo LONGITUDE]

optional arguments:
  -h, --help            show this help message and exit
  -a APP_ID, --app_id APP_ID
                        Specify iNaturalist Application ID (default: None)
  -s APP_SECRET, --app_secret APP_SECRET
                        Specify iNaturalist Application Secret (default: None)
  -u USERNAME, --username USERNAME
                        Specify iNaturalist username (default: None)
  -p PASSWORD, --password PASSWORD
                        Specify iNaturalist password (default: None)
  -d DIRECTORY, --directory DIRECTORY
                        Specify Directory path (default: None)
  -t TAXON_ID, --taxon_id TAXON_ID
                        Specify Taxon id (default: None)
  -tz TIME_ZONE, --time_zone TIME_ZONE
                        Specify Time Zone (default: Asia/Kolkata)
  -la LATITUDE, --latitude LATITUDE
                        Specify Latitude (default: None)
  -lo LONGITUDE, --longitude LONGITUDE
                        Specify Longitude (default: None)
```

## Notes

Date and coordinates with be collected from the image properties. 

If date absent in the image, current date will be used. 

If coordinates are absent, they will be kept null unless specified in the parameter.

## Example

``` python
$ python3 post_observation_dir.py -u <username>  -a <app id> -s <app secret> -d /home/test/per/CHICALIM_BIO/BIRDS/ -t 3 -la 15.399344 -lo 73.844173
Password:
```
