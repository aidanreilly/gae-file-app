#Based on GCE demo app found here:

https://cloud.google.com/appengine/docs/python/googlecloudstorageclient/getstarted

#Run with

    dev_appserver.py --default_gcs_bucket_name gcp-filebox.appspot.com app.yaml

#Features
* Upload file feature that stores files in Google Cloud Storage.
    - filename, format and a timestamp recorded in the GAE datastore
* Download file feature
* Files page displays uploaded files (timestamp and filename) is displayed. Click on checkbox and press download to download a file. 
* Upload feature on the same page.

#Requirements
* Apply CSS to somethings on the files page
* README file which descrbies how to run/install. Also detail known bugs/limitations. 
* .appspot.com URL: 