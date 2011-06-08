#!/usr/bin/python2.5

"""
Created by:
Aaron Gamble - jaarongamble@gmail.com github:aarongamble
Mahalia Miller - mahaliakmiller@gmail.com
Leon Smith - lesmith@csu.fullerton.edu
Naren Ranjit - narendran.ranjit@gmail.com
Hari Kunamneni - hkunamneni@hotmail.com (408) 417-0783
Madeleine Udell - madeleine.udell@gmail.com
"""

__author__ = 'one crisis team at RHOK #3 2011'

from google.appengine.ext import db
from google.appengine.api import users

# All fields are either required, or have a default value.  For property
# types that have a false value, the default is the false value.  For types
# with no false value, the default is None.

class Person(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    name = db.StringProperty(default='', multiline=True)
    email = db.StringProperty(default='')
    phone = db.StringProperty(default='')

    profession = db.StringProperty(default='')
    home_street = db.StringProperty(default='')
    home_neighborhood = db.StringProperty(default='')
    home_city = db.StringProperty(default='')
    home_state = db.StringProperty(default='')
    home_postal_code = db.StringProperty(default='')
    home_country = db.StringProperty(default='')
    home_address = db.StringProperty()
    home_location = db.TextProperty()
    home_latlong = db.GeoPtProperty()
    photo_url = db.TextProperty(default='')

    resource_skills = db.StringListProperty()


