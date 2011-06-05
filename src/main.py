from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
import os
import logging
from google.appengine.ext.webapp import template
from django.utils import simplejson
class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
        self.response.out.write(template.render(path, template_values))
        
class People(webapp.RequestHandler):
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
        
        if user and user.key() == person.key():
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
    @login_required
    def get(self):
        user = users.get_current_user()
        
        if not user:
            #should not ever get here since we are using @login_required
            return
        
        #Check if the user already has a person object
        person = Person.get(user.user_id())
        
        if not person:
            #Create a new Person instance for this user
            person = Person(key_name=user.key())
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
        #searchItems = []

        #grab post data
        #skill=doctor&skill=engineer.
        searchParams = self.request.get_all('skills')
        logging.debug(searchParams)

        #query data set
        #searchData = Persons.search(searchParams)


        #return simplejson.dumps(search data)
        return


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
