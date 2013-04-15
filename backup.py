# -*- coding: utf-8 -*-

import webapp2
from google.appengine.ext.db.metadata import Kind
from google.appengine.api import taskqueue

class BackupAllKinds(webapp2.RequestHandler:
    def get(self):

        # make list of all Kinds
        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write("Kinds:\n")
        kind_names = []
        q = Kind.all()
        for kind in q.fetch(100):
          if kind.kind_name[0] != "_":
              kind_names.append(kind.kind_name)
              self.response.out.write(kind.kind_name+"\n")

        # excute backup queue in backup-builtin-queue       
        params = {
        "name" : "SchduledBackup",
        "queue" : "backup-builtin-queue",
        "filesystem" : "blobstore",
        "kind" : kind_names
        }
        
        url = "/_ah/datastore_admin/backup.create"
        taskqueue.add(url=url, params=params,queue_name="backup-builtin-queue")
        
        self.response.out.write("end")

app = webapp2.WSGIApplication([
     ('/backup', BackupAllKinds)
     ],
     debug=True)