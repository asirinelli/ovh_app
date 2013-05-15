# Copyright (C) 2013 Antoine Sirinelli <antoine@monte-stello.com>
# 
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2.

import requests
import json
import time
import hashlib


class APIError(Exception):
    def __init__(self, status_code, r):
        self.status_code = status_code
        self.response = r
    def __str__(self):
        return repr(self.status_code)


class OVH_APP:
    def __init__(self, application, secret, accessRules,
                 url='https://api.ovh.com/1.0'):
        self.application = application
        self.secret = secret
        self.accessRules = accessRules
        self.url = url

    def get(self, path, custumerKey):
        return self._ovh_req(path, "GET", custumerKey)
    
    def post(self, path, custumerKey, params):
        return self._ovh_req(path, "POST", custumerKey, params)

    def delete(self, path, custumerKey):
        return self._ovh_req(path, "DELETE", custumerKey)

    def put(self, path, custumerKey, params):
        return self._ovh_req(path, "PUT", custumerKey, params)

    def request_CK(self, redirection=None):
        headers = { 'Content-type': 'application/json',
                    'X-Ovh-Application': self.application}
        params = { 'accessRules': self.accessRules}
        if redirection:
            params['redirection'] = redirection
        q = requests.post(self.url+'/auth/credential',
                          headers=headers, data=json.dumps(params))
        CK = q.json()['consumerKey']
        redirect = q.json()['validationUrl']
        return CK, redirect
        

    def _ovh_req(self, path, req_type, CK, params=None):
        now = str(int(time.time()))

        if params:
            data = json.dumps(params)
        else:
            data = ""

        url = self.url+path

        s1 = hashlib.sha1()
        s1.update("+".join([self.secret, CK, req_type, url, data, now]))
        sig = "$1$" + s1.hexdigest()

        headers = { 'Content-type': 'application/json',
                    'X-Ovh-Application':  self.application,
                    "X-Ovh-Consumer": CK,
                    'X-Ovh-Timestamp': now,
                    "X-Ovh-Signature": sig,
                    }
        if req_type == "GET":
            r = requests.get(url, headers=headers)
        elif req_type == "POST":
            r = requests.post(url, headers=headers, data=data)
        elif req_type == "DELETE":
            r = requests.delete(url, headers=headers)
        elif req_type == "PUT":
            r = requests.put(url, headers=headers, data=data)

        if r.status_code != 200:
            raise APIError(int(r.status_code), r)

        return r.json()

