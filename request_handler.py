import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_entries, get_single_entry, delete_entry, get_entry_by_search, create_entry
from urllib.parse import urlparse, parse_qs



class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # def parse_url(self, path):
        # url_components = urlparse(path) #various components broken into truple
        # path_params = url_components.path.strip("/").split("/")
        # query_param = url_components.query.split("&")
        # resource = path_params[0]
        # id = None

        # try:
        #     id = int(path_params[1])
        # except IndexError:
        #     pass
        # except ValueError:
        #     pass

        # return (resource, id, query_param)
        # add this import to the top of the file


    
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        """Handles GET requests to the server """
        response = {}
        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "entries":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_entry(id)
                else:
                    self._set_headers(200)
                    response = get_all_entries()
                
        else: 
            (resource, query) = parsed
            if query.get('entry') and resource == 'entries':
                self._set_headers(200)
                response = get_entry_by_search(query['entry'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_entry = None

        if resource == "entries":
            if (
                "concept" in post_body
                and "entry" in post_body
                and "mood_id" in post_body
                and "date" in post_body
            ):
                self._set_headers(201)
                new_entry = create_entry(post_body)
                self.wfile.write(json.dumps(new_entry).encode())
            else:
                self._set_headers(400)
                message = {
                    "message": f'{"concept is required" if "concept" not in post_body else ""}{"entry is required" if "entry" not in post_body else ""}{"mood_id is required" if "mood_id" not in post_body else ""}{"date is required" if "date" not in post_body else ""}'
                }
                self.wfile.write(json.dumps(message).encode())
        
    def do_PUT(self):
        """Handles PUT requests to the server """
        

    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)

        if resource == "entries": 
            delete_entry(id)
        
        self.wfile.write("".encode())
        

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
