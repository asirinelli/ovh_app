#!/usr/bin/env python

# Copyright (C) 2013 Antoine Sirinelli <antoine@monte-stello.com>
# 
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2.

from ovh_api import OVH_API

application = raw_input("Application: ")
applicationSecret=raw_input("Secret: ")

accessRules = [ { 'method': 'GET',
                  'path': '/sms'},
                { 'method': 'GET',
                  'path': '/sms/*'},
                { 'method': 'POST',
                  'path': '/sms/*'},
                { 'method': 'DELETE',
                  'path': '/sms/*'}]

app = OVH_APP(application, applicationSecret, accessRules)
CK, redirect = app.request_CK()
print "Please visit the link:"
print redirect
ok = raw_input("Press Enter when validated")

ids = app.get('/sms', CK)
print ids

id = ids[0]
senders = app.get('/sms/'+id+'/senders', CK)

for s in senders:
    infos = app.get("/sms/"+id+"/senders/"+s, CK)
    print s, infos['description'], infos['status']

users = app.get('/sms/'+id+'/users', CK)

for u in users:
    infos = app.get('/sms/'+id+'/users/'+u, CK)
    print u, infos['login'], infos['password']

print app.post('/sms/'+id+'/users', CK, {'login': 'deleteme',
                                         'password': 'BADpassW'})

users = app.get('/sms/'+id+'/users', CK)
for u in users:
    infos = app.get('/sms/'+id+'/users/'+u, CK)
    print infos
    print u, infos['login'], infos['password']

app.delete('/sms/'+id+'/users/deleteme', CK)
users = app.get('/sms/'+id+'/users', CK)
for u in users:
    infos = app.get('/sms/'+id+'/users/'+u, CK)
    print u, infos['login'], infos['password']
