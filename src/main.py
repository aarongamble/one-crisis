from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import os
from google.appengine.ext.webapp import template
from django.utils import simplejson

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
        self.response.out.write(template.render(path, template_values))
        
class People(webapp.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

class Profile(webapp.RequestHandler):
    def get(self):
        pass

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
        #searchParams = request.POST.get('search')

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
