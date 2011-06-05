from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
import os
import logging
from google.appengine.ext.webapp import template
from django.utils import simplejson
import distance

from model import *

Resources = {
        '1' : 'Engineering',
        '2' : 'Doctor',
        '3' : 'Food',
        '4' : 'Transportation'
}
'''
limit one person to each user
the entire code base uses this assumption
'''
USER_PERSON_LIMIT = 1

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {'resources': Resources}
        path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
        self.response.out.write(template.render(path, template_values))
        
class People(webapp.RequestHandler):
    
    @staticmethod
    def get_current_user_person():
        user = users.get_current_user()
        if not user:
            return None
        return People.get_user_person(user)
    
    @staticmethod
    def get_user_person(user):
        person = db.Query(Person).filter('user =', user).fetch(limit=USER_PERSON_LIMIT)
        if person:
            return person[0] # Only one person for each user
        else:
            return None
        
    def get(self):
        user = users.get_current_user()
        person = Person.get(self.request.get('id'))
        if not person:
            template_values = {'person':    None,
                               'user':      user,
                               'edit':      False}
            path = os.path.join(os.path.dirname(__file__), 'templates/profile.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        if person.user == user:
            edit = True     # Viewing self, mark as edit
        else:
            edit = False
        
        template_values = {'person':    person,
                           'user':      user,
                           'edit':      True}
        path = os.path.join(os.path.dirname(__file__), 'templates/profile.html')
        self.response.out.write(template.render(path, template_values))
        return

    def post(self):
        pass

class Profile(webapp.RequestHandler):
  #  @login_required
    def get(self):
        user = users.get_current_user()
        logging.debug(user)
        
        if not user:
            #should not ever get here since we are using @login_required
            return
        
        logging.debug("user")
        logging.debug(user)
        #Check if the user already has a person object
        person = People.get_current_user_person()
        
        if not person:
            #Create a new Person instance for this user
            person = Person()
            person.name = user.nickname
            person.email = user.email
            person.put()
        
        template_values = {'person': person, 'resources': Resources}
        
        path = os.path.join(os.path.dirname(__file__), 'templates/profile.html')
        self.response.out.write(template.render(path, template_values))
        

    def post(self):
        user = users.get_current_user()
        if not user:
            error(403)
        
        person = People.get_user_person(user)
        if person.user != user:
            error(403)
        
        request = self.request
        
        name = request.get('name')
        if name:
            person.name = name
            
        email = request.get('email')
        if email:
            person.email = email
        
        phone = request.get('phone')
        if phone:
            person.phone = phone
            
        home_street = request.get('home_street')
        if home_street:
            person.home_street = home_street
        
        home_neighborhood = request.get('home_neighborhood')
        if home_neighborhood:
            person.home_neighborhood = home_neighborhood
            
        home_city = request.get('home_city')
        if home_city:
            person.home_city = home_city
        
        home_state = request.get('home_state')
        if home_state:
            person.home_state = home_state
        
        home_postal_code = request.get('home_postal_code')
        if home_postal_code:
            person.home_postal_code = home_postal_code
        
        home_country = request.get('home_country')
        if home_country:
            person.home_country = home_country
            
        photo_url = request.get('photo_url')
        if photo_url:
            person.photo_url = photo_url
        
        resource_skills = request.get_all('resource_skills')
        if resource_skills:
            person.resource_skills = resource_skills
            
        person.location = Distance.getlatlong(\
          country=person.home_country,\
          state=person.home_state,\
          city=person.home_city,\
          street=person.home_street,\
          postal_code=person.home_postal_code)
          
        person.put()
        
        self.response.set_status(200)
                           
        '''
        Not sure what to do with resources
        
        #then describe the resources and limitations to that
        resource_skill = db.StringListProperty()
        location_street = db.StringProperty(default='')
        location_neighborhood = db.StringProperty(default='')
        location_city = db.StringProperty(default='')
        location_state = db.StringProperty(default='')
        location_postal_code = db.StringProperty(default='')
        location_country = db.StringListProperty()
        '''
        
        

class Search(webapp.RequestHandler):
    def get(self):
        pass


    #need to verify post name

    def post(self):
        #var to hold search Items
        emptyArray = []

        #grab post data
        #skill=doctor&skill=engineer.
        searchSkills = self.request.get_all('skills')
        searchLocation = self.request.get_all('location')

        searchResults =  db.Query(Person).filter("resource_skills IN" , searchSkills)


        searchResults = {"id":"1",
                "name":"Leon Smith",
                "location":"Long Beach",
                "matched_skills":"Sleeping"}





                #"id": "id1",
                #"name": "John Smith",
		#"location": "San Ramon, CA",
		#"matched_skills": "food, engineering"

        # Filter by distance to query
        try:
          query_location = distance.getlatlong(country=searchLocation)
          closest_people = distance.find_closest(query_location,searchResults)
        except: closest_people = {0: searchResults}

                # closest_people = {distance1: [person1,person2,...], distance2: [...]}
       
       # Results is a list of dicts.  
       # Each dict corresponds to a person with skills matching query skills, 
       # The dicts are sorted in order of increasing distance to query location
        results = ["null"]
        for distance in sorted(closest_people.keys()):
            for person in closest_people[distance]:
                results.append({"id":person.id, "name":person.name,"location":person.location, "matched_skills":person.resource_skills})




        results = {"id":"1",
                "name":"Leon Smith",
                "location":"Long Beach",
                "matched_skills":"Sleeping"}



        if len(results) > 0:
            return  self.response.out.write(simplejson.dumps(results))

        else:
            return  self.response.out.write(emptyArray)

        


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/people', People),
                                      ('/profile', Profile),
                                      ('/search', Search)],
                                     debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
