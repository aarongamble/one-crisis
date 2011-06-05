import simplejson as json
import urllib
from math import *

class Distance:
  def getDistance( lat1,lng1,lat2,lng2 ):
    '''Calculates the distance in km between the points at lat/lon pairs (lat1,lng1) and (lat2,lng2)'''
    r = 6378.137
    xyz1 = ( r*cos(lat1*pi/180)*cos(lng1*pi/180),\
                r*cos(lat1*pi/180)*sin(lng1*pi/180),\
                r*sin(lat1*pi/180) )
    xyz2 = ( r*cos(lat2*pi/180)*cos(lng2*pi/180),\
                r*cos(lat2*pi/180)*sin(lng2*pi/180),\
                r*sin(lat2*pi/180) )
    print xyz1
    print xyz2
    dxyz = map(lambda x1,x2: x1-x2, xyz1, xyz2)
    print dxyz
    distance = sqrt(sum( map( lambda x: math.pow( x, 2 ), dxyz ) ) )
    return distance
    
  def getlatlong(country='',state='',city='',street='',street_number='',postal_code=''):
    '''Returns the location information (including latitude and longitude and bounding box) for the given location information'''
    try:
      valid_fields = ['+'.join(field.split()) for field in [street_number,street,city,state,postal_code,country] if field]
      query = '+'.join(valid_fields)
      map_address = urllib.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+query+'&sensor=false').read()
      info = json.loads(map_address)
      if info['status'] == 'OK':
        return info['results'][0]
      else: return 0
    except: return 0
    
  def find_closest(location,possible_matches):
    '''Returns a dict of people close enough to the query location.  Keys are distances to query location
    closest_people = {distance1: [person1,person2,...], distance2:[], ...}'''
    closest_people = {}
    lat = location['geometry']['location']['lat']
    lng = location['geometry']['location']['lng']
    # Maximum radius in which to return results should be 10km greater than the size of the bounding box
    r = 10 + max( getDistance(lat,lng,location['geometry']['bounds']['northeast']['lat'],location['geometry']['bounds']['northeast']['lng']),
      getDistance(lat,lng,location['geometry']['bounds']['southwest']['lat'],location['geometry']['bounds']['southwest']['lng']))
    for person in possible_matches:
      lat1 = person.location['geometry']['location']['lat']
      lng1 = person.location['geometry']['location']['lng']
      distance = getDistance(lat,lng,lat1,lng1)
      if distance<r:
        if distance in closest_people:  closest_people[distance].append(person)
        else: closest_people[distance] = [person]
      return closest_people
  