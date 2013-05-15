#!/usr/bin/env python

# Copyright (C) 2013 Antoine Sirinelli <antoine@monte-stello.com>
# 
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2.

from bottle import route, run, template, request, response, redirect
from ovh_app import OVH_APP, APIError
import json

@route('/hello/<name>')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)

def get_credential():
    CK, redirection = app.request_CK(request.url)
    response.set_cookie('CK', CK)
    redirect(redirection)


@route('/sms')
def sms():
    CK = request.get_cookie('CK')
    if CK:
        try:
            ids = app.get('/sms', CK)
        except APIError as e:
            if e.status_code == 403:
                get_credential()
        id = ids[0]
        senders = app.get('/sms/'+id+'/senders', CK)
        out = [app.get('/sms/'+id+'/senders/'+s, CK) for s in senders]
        response.content_type = 'application/json'
        return json.dumps(out)

    else:
        get_credential()

@route('/cloud')
def cloud():
    CK = request.get_cookie('CK')
    if CK:
        try:
            ids = app.get('/cloud', CK)
        except APIError as e:
            if e.status_code == 403:
                get_credential()
        return ids
    else:
        get_credential()


application = raw_input("Application: ")
applicationSecret = raw_input("Secret: ")

accessRules = [ { 'method': 'GET',
                  'path': '/sms*'},
                { 'method': 'GET',
                  'path': '/cloud'}]

app = OVH_APP(application, applicationSecret, accessRules)


run(host='localhost', port=8080)
