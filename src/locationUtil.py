import urllib.request
import json
from haversine import haversine

apiKey = "AIzaSyC-IqShELxSJuURibCTsUvcm_V7mYFQeKY"


def getDistanceBetweenCoords(lat1, long1, lat2, long2):
    location1 = (lat1, long1)
    location2 = (lat2, long2)
    return haversine(location1, location2)


def extractDataFromZip(zipCode):
    request = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (zipCode, apiKey)
    response = urllib.request.urlopen(request).read().decode('utf-8')
    asJson = json.loads(response)

    state = asJson["results"][0]["address_components"][3]["short_name"]
    lat = asJson["results"][0]["geometry"]["location"]["lat"]
    lng = asJson["results"][0]["geometry"]["location"]["lng"]

    return state, lat, lng
