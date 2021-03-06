import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

from django.utils import simplejson

#local imports
import distance
from model import *

Resources = {
        '1' : 'Engineering',
        '2' : 'Doctor',
        '3' : 'Food',
        '4' : 'Transportation',
        '5' : 'Languages'
}


USER_PERSON_LIMIT = 1 #limit one person to each user.
                      #the entire code base uses this assumption
TEMPLATES_DIR = "templates"
APPLICATION_NAME = "Crisis Action Center"
_DEBUG=True

class Handler(webapp.RequestHandler):
    """
    Supplies a common template generation function.
    When you call generate(), we augment the template variables supplied with
    the current user in the 'user' variable and the current webapp request
    in the 'request' variable.
    """
    def generate(self, template_name, template_values = {}):
        values = {
            'request': self.request,
            'user': users.get_current_user(),
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url('http://%s/' % (
                self.request.host,)),
            'application_name': APPLICATION_NAME,}
        values.update(template_values)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, os.path.join(TEMPLATES_DIR, template_name))
        self.response.out.write(template.render(path, values, debug=_DEBUG))

class MainPage(Handler):
    def get(self):
        self.generate('main.html', {'resources': Resources})

class People():

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

class Profile(Handler):
    '''
    Redirects user to their own profile
    Creates one if necessary
    '''

    def get(self):

        modify = False
        id = self.request.get('id')
        if id:
            try:
                person = Person.get_by_id(int(id))
            except:
                pass

            if not person:
                # id was supplied but did not resolve to a Person
                self.error(404)
                self.response.out.write('404 id %s not found' %id)
                return
        else:
            modify = True
            person = People.get_current_user_person()
            if not person:
                self.error(404)
                self.response.out.write('404 id not supplied and you do not have an account. Visit /createprofile to create a profile')
                return

        if self.request.get('edit'):
            edit = True
        else:
            edit = False

        template_values = {'person':    person,
                           'resources': Resources,
                           'edit':      edit,
                           'modify':    modify}

        self.generate('profile.html', template_values)

    def post(self):
        user = users.get_current_user()
        if not user:
            error(403)
            return

        person = People.get_user_person(user)
        if not person or person.user != user:
            error(403)
            return

        request = self.request


        name = request.get('name')
        if name:
            person.name = name

        email = request.get('email')
        if email:
            person.email = email

        home_address = request.get('address')
        if home_address:
            person.home_address = home_address

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
        profession = request.get('profession')
        if profession:
            person.profession = profession

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
            person.resource_skills = [ skill.strip() \
                                       for skill in resource_skills \
                                       if len(skill.strip()) > 0 ]

        person.location = distance.getlatlongaddr(person.home_address)

        person.put()

        self.response.set_status(200)


class CreateProfile(Handler):
    @login_required
    def get(self):
        person = People.get_current_user_person()
        if not person:
            person = Person()
            person.name = person.user.nickname()
            person.email = person.user.email()
            person.put()
        self.redirect('/profile')


class Search(Handler):
    def get(self):
        if _DEBUG:
            self.post()

    def post(self):
        skills = [s.strip() for s in self.request.get_all('skills')]
        location = self.request.get_all('location')

        q = Person.all()
        for s in skills:
            q.filter('resource_skills =', s)

        results = q.fetch(10)

        #"id": "id1",
        #"name": "John Smith",
        #"location": "San Ramon, CA",
        #"matched_skills": "food, engineering"

        if results:
            self.response.out.write(simplejson.dumps(
                [{'id':             p.key().id(),
                  'name':           p.name,
                  'location':       p.home_location,
                  'matched_skills': p.resource_skills} for p in results]))
        else:
            self.response.out.write('[]')

        return

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/people', People),
                                      ('/profile', Profile),
                                      ('/createprofile', CreateProfile),
                                      ('/search', Search)],
                                     debug=_DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
