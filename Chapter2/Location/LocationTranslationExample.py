#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Translates a location string to coordinates using the database or Nominatim Service.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import urllib
from Chapter2.support.Location import Location
import requests
import argparse


class LocationTranslationExample(object):
    def __init__(self):
        pass

    def translate_loc(self, loc):
        """
        Translates a location string to coordinates using the database or Nominatim Service
        Example: loc Brickyard Building Tempe 85281 translates to Latitude: 33.4236 & Longitude: -111.9396
        :type loc: string
        :param loc - location
        :return - Location("lat","lon")
        """
        location = "No Result"
        print "Location", loc
        if not loc:
            return
        encoded_loc = urllib.quote(loc.encode('utf8'))
        url = "http://open.mapquestapi.com/nominatim/v1/search?q=" + encoded_loc + "&format=json" + "&key=0EbGZdPxMd7G80nIqadYzgVD0EfL9RtX";
        results = self.read_html(url)
        if not results:
            return location
        if len(results) > 0:
            location = Location(results[0]['lat'], results[0]['lon'])

        return location

    def read_html(self, url):
        """
        Makes Request and gets Content
        :param url: 
        :return: JSON result object
        """
        r = requests.get(url=url)
        if r.status_code == 404 or r.status_code == 400:
            print "Error", r.content
            return ""
        if r.status_code == 403:
            print "Authorization Error"
            return ""

        return r.json()


def main(args):
    """
    Creates a LocationTranslationExample object and translates the location string ( given in args ) to Latitude and 
    Longitude. 
    """
    parser = argparse.ArgumentParser(
        description='''Creates user access token and secret and saves it into config.json. Also verifies the key.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('locationString', nargs="?", default="Brickyard Building Tempe 85281",
                        help='Give the location string/address')
    argsi = parser.parse_args()
    lte = LocationTranslationExample()
    print lte.translate_loc(argsi.locationString)


if __name__ == "__main__":
    main(sys.argv)
