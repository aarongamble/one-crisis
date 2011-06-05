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

'''
limit one person to each user
the entire code base uses this assumption
'''
USER_PERSON_LIMIT = 1

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
        self.response.out.write(template.render(path, template_values))
        
class People(webapp.RequestHandler):
    
    @staticmethod
    def get_current_user_person():
        user = users.get_current_user()
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
            person.put()
        
        template_values = {'person': person}
        
        path = os.path.join(os.path.dirname(__file__), 'templates/profile.html')
        self.response.out.write(template.render(path, template_values))
        

    def post(self):
        pass

class Search(webapp.RequestHandler):
    def get(self):
        pass


    #need to verify post name

    def post(self):
        #var to hold search Items
        searchItems = []

        #grab post data
        #skill=doctor&skill=engineer.
        searchSkills = self.request.get_all('skills')
        searchLocation = self.request.get_all('location')

        searchResults = Person.objects.filter(resource_skill__in = searchSkills)


                #"id": "id1",
                #"name": "John Smith",
		#"location": "San Ramon, CA",
		#"matched_skills": "food, engineering"

        # Filter by distance to query
        query_location = Distance.getlatlng(country=searchLocation)
        closest_people = Distance.find_closest(query_location,searchResults)

        # closest_people = {distance1: [person1,person2,...], distance2: [...]}

        results = []
        for distance in sorted(closest_people.keys()):
            for person in closest_people[distance]:
                results.append({"id":person.id, "name":person.name,"location":person.location, "matched_skills":person.resource_skill})


        return simplejson.dumps(results)
        
       


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/people', People),
                                      ('/profile', Profile),
                                      ('/search', Search)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
