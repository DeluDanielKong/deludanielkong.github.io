

# # Leaflet cluster map of talk locations
#
# (c) 2016-2017 R. Stuart Geiger, released under the MIT license
#
# Run this from the _talks/ directory, which contains .md files of all your talks. 
# This scrapes the location YAML field from each .md file, geolocates it with
# geopy/Nominatim, and uses the getorg library to output data, HTML,
# and Javascript for a standalone cluster map.
#
# Requires: glob, getorg, geopy
import glob
import getorg
from geopy import Nominatim

g = glob.glob("*.md")

# 添加 user_agent
geocoder = Nominatim(user_agent="my-talks-map")
location_dict = {}

for file in g:
    with open(file, 'r') as f:
        lines = f.read()
        if 'location: "' in lines:
            loc_start = lines.find('location: "') + 11
            lines_trim = lines[loc_start:]
            loc_end = lines_trim.find('"')
            location = lines_trim[:loc_end].strip()
            
            # 添加异常处理，防止地址无效或 geocoding 失败
            try:
                geo_result = geocoder.geocode(location)
                if geo_result:
                    location_dict[location] = geo_result
                    print(location, "\n", geo_result)
                else:
                    print("Could not geocode:", location)
            except Exception as e:
                print("Error geocoding", location, ":", e)

m = getorg.orgmap.create_map_obj()
getorg.orgmap.output_html_cluster_map(location_dict, folder_name="../talkmap", hashed_usernames=False)
