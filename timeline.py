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
	print "Created: " + post.get("created_time")
	print "Post ID: " + post.get("id")
	feed_comment = graph.get_connections(post.get("id"), "comments")
	for comment in feed_comment['data']:
		print "++++"
		print comment['from'].get("name")
		print comment.get("message")
		print "Created: " + comment.get("created_time")
	print "------------------"
