#!/usr/bin/env python

# Copyright 2017 Google Inc.
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

# [START sample]
"""A sample app that uses GCS client to operate on bucket and file."""

# [START imports]
import os

import cloudstorage
from google.appengine.api import app_identity

import webapp2

# [END imports]

# [START retries]
cloudstorage.set_default_retry_params(
    cloudstorage.RetryParams(
        initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=15
        ))
# [END retries]


class MainPage(webapp2.RequestHandler):
    """Main page for GCS demo application."""

# [START get_default_bucket]
    def get(self):
        bucket_name = os.environ.get(
            'gcp-filebox.appspot.com', app_identity.get_default_gcs_bucket_name())

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(
            'Demo GCS Application running from Version: {}\n'.format(
                os.environ['CURRENT_VERSION_ID']))
        self.response.write('Using bucket name: {}\n\n'.format(bucket_name))
# [END get_default_bucket]

        bucket = '/' + bucket_name
        filename = bucket + '/demo-testfile'
        self.tmp_filenames_to_clean_up = []

        self.list_bucket(bucket)
        self.response.write('\n\n')

        self.list_bucket_directory_mode(bucket)
        self.response.write('\n\n')


# [START list_bucket]
    def list_bucket(self, bucket):
        """Create several files and paginate through them."""

        self.response.write('Listbucket result:\n')

        # Production apps should set page_size to a practical value.
        page_size = 1
        stats = cloudstorage.listbucket(bucket + '/foo', max_keys=page_size)
        while True:
            count = 0
            for stat in stats:
                count += 1
                self.response.write(repr(stat))
                self.response.write('\n')

            if count != page_size or count == 0:
                break
            stats = cloudstorage.listbucket(
                bucket + '/foo', max_keys=page_size, marker=stat.filename)
# [END list_bucket]

    def list_bucket_directory_mode(self, bucket):
        self.response.write('Listbucket directory mode result:\n')
        for stat in cloudstorage.listbucket(bucket + '/b', delimiter='/'):
            self.response.write(stat)
            self.response.write('\n')
            if stat.is_dir:
                for subdir_file in cloudstorage.listbucket(
                        stat.filename, delimiter='/'):
                    self.response.write('  {}'.format(subdir_file))
                    self.response.write('\n')

app = webapp2.WSGIApplication(
    [('/', MainPage)], debug=True)
# [END sample]
