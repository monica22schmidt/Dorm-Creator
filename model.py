  
from google.appengine.ext import ndb

class User(ndb.Model):
    user_id = ndb.StringProperty()
    color = ndb.StringProperty()
    style = ndb.StringProperty()
    gender = ndb.StringProperty()
    extras = ndb.StringProperty()
