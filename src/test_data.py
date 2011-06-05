from model import *
from main import *


def test_data():
    person = Person(user = None,
                name = 'Alice',
                email = 'alice@alice.com',
                phone = '1-800-alice',
                home_street = '100 University Ave',
                #home_neighborhood = db.StringProperty(default='')
                home_city = 'San Francisco',
                home_state = 'California',
                home_postal_code = '',
                home_country = '')
    
    person.put()
