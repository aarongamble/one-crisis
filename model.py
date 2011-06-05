#!/usr/bin/python2.5
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
import config
import indexing
import pfif
import prefix

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
    author_name = db.StringProperty(default='', multiline=True)
    author_email = db.StringProperty(default='')
    author_phone = db.StringProperty(default='')
    home_city = db.StringProperty(default='')
    home_country = db.StringProperty(default='')
    
    home_street = db.StringProperty(default='')
    home_neighborhood = db.StringProperty(default='')
    home_city = db.StringProperty(default='')
    home_state = db.StringProperty(default='')
    home_postal_code = db.StringProperty(default='')
    home_country = db.StringProperty(default='')
    photo_url = db.TextProperty(default='')
    description = db.TextProperty(default='', multiline=True)
    
    resource_skill = db.StringListProperty()
    location_street = db.StringProperty(default='')
    location_neighborhood = db.StringProperty(default='')
    location_city = db.StringProperty(default='')
    location_state = db.StringProperty(default='')
    location_postal_code = db.StringProperty(default='')
    location_country = db.StringListProperty()

class Resource():
    it_provider = db.BooleanProperty()
    med_provider = db.BooleanProperty()
    engineer = db.BooleanProperty()
    farmer = db.BooleanProperty()
    interpreter = db.BooleanProperty()
    project_manager = db.BooleanProperty()
    hr_manager = db.BooleanProperty()
    logistics = db.BooleanProperty()
    otherProvider = db.BooleanProperty()
    
    water = db.BooleanProperty()
    food = db.BooleanProperty()
    it_equipment = db.BooleanProperty()
    med_supplies = db.BooleanProperty()
    transportation = db.BooleanProperty()
    money = db.BooleanProperty()
    other = db.BooleanProperty()
