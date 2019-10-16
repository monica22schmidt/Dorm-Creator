from google.appengine.ext import ndb
# from post import Post
class User(ndb.Model):
    username=ndb.StringProperty()
    description=ndb.TextProperty()
    # following=ndb.KeyProperty('User', repeated=True)
    # posts=ndb.KeyProperty(Post)
