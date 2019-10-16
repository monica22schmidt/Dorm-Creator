
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from model import User
from google.appengine.api import users
import webapp2
import jinja2
import os



jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
class MainHandler(webapp2.RequestHandler):
    def get(self):
        my_template=jinja_environment.get_template("templates/mainpage.html")
        self.response.write(my_template.render())

class LinkHandler(webapp2.RequestHandler):
    def get(self):
        my_template=jinja_environment.get_template("templates/link.html")
        self.response.write(my_template.render())
class UsefulHandler(webapp2.RequestHandler):
    def get(self):
        my_template=jinja_environment.get_template("templates/UsefulItems.html")
        self.response.write(my_template.render())
class MatchHandler(webapp2.RequestHandler):
    def get(self):

        template = jinja_environment.get_template("templates/matchpage.html")
        render_dict = {}
        render_dict["color"] = self.request.get("Color")
        render_dict["gender"] = self.request.get("Gender")
        render_dict["style"] = self.request.get("Style")
        render_dict["extras"] = self.request.get("Extras")
        self.response.write(template.render(render_dict))
        # Color = self.request.get("color")
        # Style = self.request.get("style")
        # Gender = self.request.get("gender")



class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect("/match")
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/match'))

            self.response.write('<html><body>%s</body></html>' % greeting)
class GalleryHandler(webapp2.RequestHandler):
    def load_gallery(self, new_roomset=None):
        current_user = users.get_current_user()
        get_saved_data=User.query(User.user_id == current_user.user_id())
        saved_data=get_saved_data.fetch()
        if new_roomset:
            roomset1=False
            for x in saved_data:
                if x.key == new_roomset.key:
                    roomset1=True
            if not roomset1:
                saved_data.append(new_roomset)

        render_data={}
        render_data["saved_sets"]=saved_data
        render_data["length"]=len(saved_data)
        my_template=jinja_environment.get_template("templates/gallery.html")
        self.response.write(my_template.render(render_data))

    def post(self):
        user = users.get_current_user()
        my_output = User(user_id=user.user_id(),
            color = self.request.get("save_color"),
            style = self.request.get("save_style"),
            gender = self.request.get("save_gender"),
            extras = self.request.get("save_extras")
        )
        my_output.put()

        self.load_gallery(my_output)
    def get(self):
        self.load_gallery()
# class LoadingHandler(webapp2.RequestHandler):
#     def get(self):
#         my_template=jinja_environment.get_template("templates/Loading.html")
#         self.response.write(my_template.render())


app = webapp2.WSGIApplication([
    ('/link', LinkHandler),
    ('/', MainHandler),
    ('/match', MatchHandler),
    ('/login', LoginPage),
    ('/Use', UsefulHandler),
    ('/gallery', GalleryHandler),

], debug=True)

