#!/usr/bin/python
import os.path
import json
import urllib2
import urllib
import urlparse
import BaseHTTPServer
import webbrowser

def file_get_contents(filename):
        with open(filename) as f:
                return f.read()

 
APP_ID = file_get_contents("client_id.conf")
APP_SECRET = file_get_contents("client_secret.conf")
ENDPOINT = 'graph.facebook.com'
REDIRECT_URI = 'http://10.5.0.20:8080/'
ACCESS_TOKEN = None
LOCAL_FILE = '.fb_access_token'
STATUS_TEMPLATE = u"{name}\033[0m: {message}"

def get_url(path, args=None):
    args = args or {}
    if ACCESS_TOKEN:
        args['access_token'] = ACCESS_TOKEN
    if 'access_token' in args or 'client_secret' in args:
        endpoint = "https://"+ENDPOINT
    else:
        endpoint = "http://"+ENDPOINT
    return endpoint+path+'?'+urllib.urlencode(args)
 
def get(path, args=None):
    return urllib2.urlopen(get_url(path, args=args)).read()
 
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
 
    def do_GET(self):
        global ACCESS_TOKEN
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
 
        code = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('code')
	print code
        code = code[0] if code else None
        if code is None:
            self.wfile.write("Sorry, authentication failed.")
            sys.exit(1)
        print "-=Doing Response=-"
	response = get('/oauth/access_token', {'client_id':APP_ID,
                                               'redirect_uri':REDIRECT_URI,
                                               'client_secret':APP_SECRET,
                                               'code':code})
        print "-=Parsing Response=-"
	ACCESS_TOKEN = urlparse.parse_qs(response)['access_token'][0]
        open(LOCAL_FILE,'w').write(ACCESS_TOKEN)
        self.wfile.write("You have successfully logged in to facebook. "
                         "You can close this window now.")
 
def print_status(item, color=u'\033[1;35m'):
    print color+STATUS_TEMPLATE.format(name=item['from']['name'],
                                       message=item['message'].strip())
 
if __name__ == '__main__':
    if not os.path.exists(LOCAL_FILE):
        print "Logging you in to facebook..."
        print(get_url('/oauth/authorize',
                                {'client_id':APP_ID,
                                 'redirect_uri':REDIRECT_URI,
                                 'scope':'read_stream,publish_stream,friends_status,user_about_me'}))
 
        httpd = BaseHTTPServer.HTTPServer(('10.5.0.20', 8080), RequestHandler)
        while ACCESS_TOKEN is None:
            httpd.handle_request()
    else:
        ACCESS_TOKEN = file_get_contents(LOCAL_FILE)
    for item in json.loads(get('/me/feed'))['data']:
        if item['type'] == 'status':
            print_status(item)
            if 'comments' in item:
                for comment in item['comments']['data']:
                    print_status(comment, color=u'\033[1;33m')
            print '---'

