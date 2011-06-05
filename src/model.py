#!/usr/bin/python2.5

"""The Volunteer Finder data model
Created by:
Aaron Gamble - jaarongamble@gmail.com github:aarongamble
Mahalia Miller - mahaliakmiller@gmail.com
Leon Smith - lesmith@csu.fullerton.edu
Naren Ranjit - narendran.ranjit@gmail.com
Hari Kunamneni - hkunamneni@hotmail.com (408) 417-0783
Madeleine Udell - madeleine.udell@gmail.com"""

__author__ = 'one crisis team at RHOK #3 2011'

from datetime import timedelta

from google.appengine.api import datastore_errors
from google.appengine.api import memcache
from google.appengine.ext import db

# All fields are either required, or have a default value.  For property
# types that have a false value, the default is the false value.  For types
# with no false value, the default is None.

class Base(db.Model):
    """Base class providing methods common to both Person and Need entities."""


class Person(Base):
    """The datastore entity kind for storing a PFIF person record.  Never call
    Person() directly; use Person.create_clone() or Person.create_original().

    Methods that start with "get_" return actual values or lists of values;
    other methods return queries or generators for values.
    """
    # If you add any new fields, be sure they are handled in wipe_contents().

#    # entry_date should update every time a record is created or re-imported.
#    entry_date = db.DateTimeProperty(required=True)
#    expiry_date = db.DateTimeProperty(required=False)
    #basic info
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
    photo_url = db.TextProperty(default='')

    #then describe the resources and limitations to that
    resource_skill = db.StringListProperty(default='')
    address = db.StringProperty(default='')
    location_street = db.StringProperty(default='')
    location_neighborhood = db.StringProperty(default='')
    location_city = db.StringProperty(default='')
    location_state = db.StringProperty(default='')
    location_postal_code = db.StringProperty(default='')
    location_country = db.StringProperty()
