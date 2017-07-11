from os import sys, path
import urllib
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter2.support.Location import Location
import requests


class LocationTranslationExample(object):

    def __init__(self):
        pass

    def TranslateLoc(self,loc):
        if not loc:
            return
        encodedLoc = urllib.quote(loc.encode('utf8'))
        url = "http://open.mapquestapi.com/nominatim/v1/search?q=" + encodedLoc + "&format=json" + "&key=0EbGZdPxMd7G80nIqadYzgVD0EfL9RtX";
        results = self.ReadHTML(url)
        if not results:
            return

        if len(results) > 0:
            location = Location(results[0]["lat"],results[0]["lon"])

        return location

    def ReadHTML(self,url):
        r = requests.get(url=url)
        if r.status_code == 404 or r.status_code == 400:
            print "Error",r.content
            return ""
        if r.status_code == 403:
            print "Authorization Error"
            return ""

        return r.json()

def main(args):
    lte = LocationTranslationExample()
    if args!=None:
        if len(args) != 0:
            for i in range(len(args)):
                print lte.TranslateLoc(args[i])
        else:
            print lte.TranslateLoc("Brickyard Building Tempe 85281")

if __name__ == "__main__":
    main(sys.argv[1:])
