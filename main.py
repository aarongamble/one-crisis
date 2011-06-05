from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')

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

    def post(self):
        pass


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
