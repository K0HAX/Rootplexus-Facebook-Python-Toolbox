#!/usr/bin/python
import facebook

def file_get_contents(filename):
	with open(filename) as f:
		return f.read()

token = file_get_contents(".fb_access_token")

graph = facebook.GraphAPI(token)
profile = graph.get_object("me")

my_status = raw_input("Status: ")
graph.put_object("me", "feed", message=my_status)

