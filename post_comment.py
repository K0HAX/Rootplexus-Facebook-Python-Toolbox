#!/usr/bin/python
import facebook

def file_get_contents(filename):
        with open(filename) as f:
                return f.read()

token = file_get_contents(".fb_access_token")

graph = facebook.GraphAPI(token)
profile = graph.get_object("me")

status_id = raw_input("Post ID: ")
my_comment = raw_input("Comment: ")
graph.put_object(status_id, "comments", message=my_comment)

