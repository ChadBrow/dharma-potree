import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# 8000 doesn't mean anything, feel free to change to any other 4 digit number
PORT = 8000


# if you haven't seen this syntax before, it's Python's inheritance,
# and in this case it means MyHandler extends BaseHTTPRequestHandler
class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)  # 200 stands for request succeeded
        self.send_header("Content-type", "text/html")  # informs requests of the Media type
        self.end_headers()

    # entering the localhost url into your browser, you will get an additional /favicon.ico path,
    # so take this into account with testing.
    # this method is where
    def do_GET(self):
        self._set_headers()
        print(self.path)  # if url is localhost:8000/test, self.path would equal '/test'
        if self.path == '/hello-there':
            json_string = json.dumps({'hello': 'back', 'received': 'ok'})  # converts dictionary to a JSON string
            self.wfile.write(json_string.encode(encoding='utf_8'))  # like before, encode to avoid TypeError
            # the above line is what actually sends data back to client on a request for data


def run(server_class=HTTPServer, handler_class=MyHandler, addr="localhost", port=PORT):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")  # f before string allows special formatting
    httpd.serve_forever()


# the next line basically checks if your configurations set this file as the "main" file,
# and if so, run the following code.
# if this code is imported into another project, that means the following code won't run,
# because this file is not the main file.
if __name__ == "__main__":
    thread = threading.Thread(target=run)
    # if threading isn't used, all code after serve_forever() (line 43) would not run
    thread.start()
    url = f'http://localhost:{PORT}/hello-there'
    request = requests.get(url)
    print(request.json())