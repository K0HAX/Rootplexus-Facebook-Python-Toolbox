#!/usr/bin/python
import facebook

def file_get_contents(filename):
        with open(filename) as f:
                return f.read()

token = file_get_contents(".fb_access_token")

graph = facebook.GraphAPI(token)
profile = graph.get_object("me")
news_feed = graph.get_connections("me", "home")

for post in reversed(news_feed['data']):
	print post['from'].get("name")
	print post.get("message")
	print post.get("created_time")
	print "------------------------"

