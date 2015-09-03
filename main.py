# Copyright 2012 Digital Inspiration
# http://www.labnol.org/

import os
import datetime
import time
import webapp2
from webapp2_extras import sessions
from google.appengine.ext import ndb
from google.appengine.ext import db
import jinja2
import sys
import cgi

# Setting up the Jinja environment to include html pages as templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#SessionConfig
config = {}
config['webapp2_extras.sessions'] = {
   'secret_key': 'aKljidLfjG3CqSDFIQ8lds1134',
   'session_max_age': None
}


def Candidate_key(candidate = "candidate"):
    return ndb.Key("candidate", candidate)

class Candidate(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    timestamp = ndb.DateTimeProperty(auto_now=True, indexed=True)


#SessionHandler
class BaseHandler(webapp2.RequestHandler):              
    def dispatch(self):                                 
        self.session_store = sessions.get_store(request=self.request)
        try:  
            webapp2.RequestHandler.dispatch(self)       
        finally:        
            self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()
      
class Logout(BaseHandler):
    def get(self):
        try:
            self.session.pop('user')
            self.response.write(self.session.get('user'))
            self.redirect('/')
        except Exception, e:
            self.response.write("No Session Stored !" + str(e))

class MainHandler(webapp2.RequestHandler):
  def get (self):
    template_values = {}        
    template = JINJA_ENVIRONMENT.get_template('login.html')
    self.response.write(template.render(template_values))

class CourseHandler(BaseHandler):
  def get(self):
    if self.session.get('user') == None:
      self.redirect('/')
    template_values = {}        
    template = JINJA_ENVIRONMENT.get_template('Course_page.html')
    self.response.write(template.render(template_values))

class SessionHandler(BaseHandler):
  def post(self):
    useremail = self.request.get("email")
    flag = False
    if useremail != None:
      self.session['user'] = useremail
      self.session['loggedin'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
      flag = True
      keycontent = self.request.get("candidate", "candidate")
      datas = Candidate(parent=Candidate_key(keycontent))
      datas.email = useremail
      datas.put()
    self.response.write(flag)

def EVS_key(EVS = "EVS"):
    return ndb.Key("EVS", EVS)

class EVS(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    title = ndb.StringProperty(indexed=True)
    timestamp = ndb.StringProperty(indexed=True)
    
class LogboxHandler(BaseHandler):
  def post(self):
    if self.session.get('user') == None:
      self.redirect('/')
    else:
      username = self.session.get('user')
      titlestr = self.request.get('title')
      ts = self.request.get('ts')
      keycontent = self.request.get('EVS', 'EVS')
      datas = EVS(parent=EVS_key(keycontent), email=self.session.get('user'), title=titlestr, timestamp=ts)
      datas.put()
      self.response.write(datas)
      self.response.write(username+" "+titlestr+" "+ts)

app = webapp2.WSGIApplication ([
  ('/', MainHandler),
  ('/Course_page', CourseHandler),
  ('/addSession', SessionHandler),
  ('/logout', Logout),
  ('/logbox', LogboxHandler)
  ], debug=True, config=config)
