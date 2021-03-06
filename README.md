# Based on GCE demo app found here:

https://cloud.google.com/appengine/docs/python/googlecloudstorageclient/getstarted

# git-hub

https://github.com/aidanreilly/gae-file-app

# config and install

The application runs in python 2

    pipenv install requests

# Features
* Upload file feature that stores files in Google Cloud Storage.
    - filename, format and a timestamp recorded in the GAE datastore
* Download file feature
* Files page displays uploaded files (timestamp and filename) is displayed. Click on checkbox and press download to download a file. 
* Upload feature on the same page

# Requirements
* Apply CSS to somethings on the files page
* README file which describes how to run/install. Also detail known bugs/limitations. 
* .appspot.com URL: https://gae-file-app.appspot.com/

# Bugs

* Uploaded bucket files are not displayed
* download files feature not working, files are uploaded however - See files_upload.png for details.

# Run the application

    dev_appserver.py --default_gcs_bucket_name gae-files-app.appspot.com app.yaml

Run locally:
    
    dev_appserver.py app.yaml

Clear the local datastore
    
    dev_appserver.py --clear_datastore=yes app.yaml

To deploy

    gcloud app deploy app.yaml --project gae-file-app

To remove an app (and project)

    IAM & Admin --> Settings --> Shut Down

Run locally
    
    dev_appserver.py app.yaml --enable_console

Set up storage and run main.py

    dev_appserver.py --default_gcs_bucket_name gae-file-app.appspot.com app.yaml --enable_console
