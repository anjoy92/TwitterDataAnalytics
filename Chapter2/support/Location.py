class Location(object):

    def __init__(self,lat,lng):
        self.latitude = float(lat)
        self.longitude = float(lng)

    def __str__(self):
        return "Latitude: " + str(self.latitude) + " & Longitude: " + str(self.longitude)