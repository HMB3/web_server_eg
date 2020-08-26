A minimal HTTP server in python. It sends a JSON Hello World for GET requests, and echoes back JSON for POST requests.

```
python server.py 8009
Starting httpd on port 8009...
```

```
curl http://localhost:8009
{"received": "ok", "hello": "world"}
```

```
curl --data "{\"this\":\"is a test\"}" --header "Content-Type: application/json" http://localhost:8009
{"this": "is a test", "received": "ok"}
```

Adapted from [this Gist](https://gist.github.com/bradmontgomery/2219997), with the addition of code for reading the request body taken from [this article](http://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/).

Please be careful when using a server like this on production environments, because it lacks many important features (threading to name one). You can consult [the python documentation about BaseHTTPServer](https://docs.python.org/2/library/basehttpserver.html) to learn something useful to improve it.

If you are on Ubuntu, you can install this code as a service with an init script (hopefully, with some modifications that make it actually do something useful). Just modify the include `server.conf` to suit your needs (possibly renaming it and redirecting output to some log files instead of `/dev/null`), and copy it into `/etc/init/`. You can then start/stop/restart the server with the usual `service` command:

```
sudo service server start
```

You also need to install python 3, and these packages : 
http.server,
http,
json
time


```
#!/usr/bin/env python3
"""An example HTTP server with GET and POST endpoints."""
from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time


# Sample blog post data similar to
# https://ordina-jworks.github.io/frontend/2019/03/04/vue-with-typescript.html#4-how-to-write-your-first-component
_g_posts = [
    {
        'title': 'My first blogpost ever!',
        'body': 'Lorem ipsum dolor sit amet.',
        'author': 'Elke',
        'date_ms': 1593607500000,  # 2020 July 1 8:45 AM Eastern
    },
    {
        'title': 'Look I am blogging!',
        'body': 'Hurray for me, this is my second post!',
        'author': 'Elke',
        'date_ms': 1593870300000, # 2020 July 4 9:45 AM Eastern
    },
    {
        'title': 'Another one?!',
        'body': 'Another one!',
        'author': 'Elke',
        'date_ms': 1594419000000, # 2020 July 10 18:10 Eastern
    }
]


class _RequestHandler(BaseHTTPRequestHandler):
    # Borrowing from https://gist.github.com/nitaku/10d0662536f37a087e1b
    def _set_headers(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps(_g_posts).encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        message['date_ms'] = int(time.time()) * 1000
        _g_posts.append(message)
        self._set_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

    def do_OPTIONS(self):
        # Send allow-origin header for preflight POST XHRs.
        self.send_response(HTTPStatus.NO_CONTENT.value)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()


def run_server():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
```
