#Simple GCE app to handle files on Google cloud storage 
#
#note to self: try out some of the other demos blob, guestbook etc.
#C:\git\appengine-guestbook-python has the info on css fixup
#C:\git\python-docs-samples\appengine\standard\blobstore\api for file uploads
#to deploy gcloud app deploy app.yaml
#datastore (relational db) and cloudstore (for actual files)
#
#[START imports]
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import app_identity
import webapp2
import logging
import os
import cgi
import urllib
from os import path
import cloudstorage as gcs
#[END imports]

#[START retries]
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
#[END retries]

class File(db.Model):
    author = db.StringProperty(multiline=True)
    content = db.BlobProperty()
    fileObj = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add = True)

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    files = File.all().order("-date").fetch(10)
    context = {
      'user': user,
      'files':  files,
      'login':  users.create_login_url(self.request.uri),
      'logout': users.create_logout_url(self.request.uri),
      }
    # [START form]
 
    tmpl = path.join( path.dirname(__file__), "html/index.html" )
    self.response.out.write( template.render(tmpl, context) )
    self.response.write('\n\n')
    self.response.out.write("""
      <form action="/upload?%s"
            enctype="multipart/form-data"
            method="post">
        <div><label>File upload:</label></div>
        <div><input type="file" name="content"/></div>
        <div><input type="submit" name="Upload"/></div>
      </form>
      <hr>""")
    tmpl = path.join( path.dirname(__file__), "html/footer.html" )
# [END form] 


class Upload(webapp2.RequestHandler):
  #this class has a function to post the file to the store from the method=post declation above
  def post(self):
    file = File()
    user = users.get_current_user()
    if user:
      file.author = user
    file.content = self.request.get("content")
    file.put()                                 
    #self.response.write("<p>You uploaded:</p> %s" % self.request.get("content")
    #self.redirect("/")

app = webapp2.WSGIApplication([ ('/', MainPage), ('/upload', Upload) ], debug=True)
