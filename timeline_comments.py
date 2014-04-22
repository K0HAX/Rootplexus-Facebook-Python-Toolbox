#!/usr/bin/python
import facebook

def file_get_contents(filename):
        with open(filename) as f:
                return f.read()

token = file_get_contents(".fb_access_token")

graph = facebook.GraphAPI(token)
profile = graph.get_object("me")
status_id = raw_input("Post ID: ")
news_feed = graph.get_connections(status_id, "comments")

for comment in news_feed['data']:
	print comment['from'].get("name")
	print comment.get("message")
	print "Created: " + comment.get("created_time")
	print "------------------------"

