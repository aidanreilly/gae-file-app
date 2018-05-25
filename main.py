#Simple GCE app to handle files on Google cloud storage 
#to deploy gcloud app deploy app.yaml
#datastore (relational db) and cloudstore (for actual files)
#
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.api import app_identity
import webapp2
import logging
import os
import cgi
import urllib
from os import path
import cloudstorage as gcs


#[START retries]
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
#[END retries]

#store objects in the db as blobs
class FileInfo(db.Model):
    blob = blobstore.BlobReferenceProperty(required=True)
    uploaded_by = db.UserProperty(required=True)
    uploaded_at = db.DateTimeProperty(required=True, auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        #creates the bucket
        bucket_name = os.environ.get('gae-file-app.appspot.com', app_identity.get_default_gcs_bucket_name())
        #holds the bucket name that we just created
        bucket = '/' + bucket_name
        # [START upload_url]
        upload_url = blobstore.create_upload_url('/upload_file')
        # [END upload_url]
        # gets current user
        user = users.get_current_user()
        files =  bucket #this is incorrect
        #how can i query the db and return list?
        #this should pull the files info in the bucket
        dl = self.request.get_all('file')
        for blob in dl:
            blob_url = str(urllib.unquote(blob))
            blob_info = blobstore.BlobInfo.get(blob_url)
            self.send_blob(blob_info, save_as=blob_info.filename)
        context = {
          'user': user,
          'files':  files,
          'login':  users.create_login_url(self.request.uri),
          'logout': users.create_logout_url(self.request.uri),
          }

        tmpl = path.join( path.dirname(__file__), "html/index.html" )
        #write the html
        self.response.out.write( template.render(tmpl, context) )
        #how to return the objects in the store???
        #show the contents of the bucket
        self.list_bucket(bucket)
        #end show contents
        self.response.write('\n\n')
        # To upload files to the blobstore, the request method must be "POST"
        # and enctype must be set to "multipart/form-data".
        self.response.out.write("""
            <html><body>
            <form action="{0}" method="POST" enctype="multipart/form-data">
              Upload File: <input type="file" name="file"><br>
              <input type="submit" name="submit" value="Submit">
            </form>
            </body></html>""".format(upload_url))
            # [END upload_form]
        tmpl = path.join( path.dirname(__file__), "html/footer.html" )


    #[START list_bucket]
    def list_bucket(self, bucket):
        page_size = 1
        stats = gcs.listbucket(bucket, max_keys=page_size)
        while True:
            count = 0
            for stat in stats:
                count += 1
                self.response.write(repr(stat))
                self.response.write('\n')
            if count != page_size or count == 0:
                break
                stats = gcs.listbucket(bucket, max_keys=page_size, marker=stat.filename)
    #[END list_bucket]

# [END form] 

# [START upload_handler]
class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        
        user=users.get_current_user().user_id()
        html = html + template.render('html/index.html', {'file':file.blob, 'key':file.blob.key()})
        upload_url = blobstore.create_upload_url('/upload')
        html = html + template.render('html/footer.html', {'upload_url':upload_url})
        self.redirect(users.create_login_url(self.request.uri)) 
        self.redirect("/")
    
# [START download_handler]
class FileDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        dl = self.request.get_all('file')
        for blob in dl:
            blob_url = str(urllib.unquote(blob))
            blob_info = blobstore.BlobInfo.get(blob_url)
            self.send_blob(blob_info, save_as=blob_info.filename)
# [END download_handler]

        
app = webapp2.WSGIApplication([ 
    ('/', MainPage), 
    ('/upload', FileUploadHandler),
    ('/download/([^/]+)?', FileDownloadHandler)
], debug=True)
