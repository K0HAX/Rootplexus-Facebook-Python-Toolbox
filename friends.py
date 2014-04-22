#!/usr/bin/python
import facebook
import json

def file_get_contents(filename):
        with open(filename) as f:
                return f.read()

token = file_get_contents(".fb_access_token")

graph = facebook.GraphAPI(token)
profile = graph.get_object("me")
friends = graph.get_connections("me", "friends")

# friends_list = [friend['name'] for friend in friends['data']]

# print friends_list
# print profile['id']

for friend in sorted(friends['data'], key=lambda friend:friend['name']):
	print friend['name']

