#!/usr/bin/env python3
"""
http_webserver

A web server to echo back a request's headers and data

"""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
import random
import time
from tornado.options import define, options, parse_command_line

# local module
import generate_job_details

# define command-line inputs
define("host", default="127.0.0.1", help="bind server to this host (e.g. 127.0.0.1)", type=str)
define("port", default=8000, help="connect to server on this port", type=int)
define("max_jobs", default=2000, help="max number of jobs", type=int)
define("delay_min", default=1, help="minimum artificial delay for GET requests (units: seconds)", type=float)
define("delay_max", default=10, help="maximum artificial delay for GET requests (units: seconds)", type=float)
define("input_file", default="jobDetails.json", help="file path to JSON data that will be fetched", type=str)

# global variable to hold local data in RAM
local_db = dict()


def load_local_data(input_file):
    """Load local data into memory
    Since data is loaded into a global variable, there should be no need to call this more than once

    :param str input_file: file path to local JSON data
    """
    global local_db

    # load job details from file
    with open(input_file) as f:
        local_db = json.load(f)


def fetch_local_data(key):
    """fetch uuid from local database using a provided key
    i.e., this is just a getter function for memory in RAM

    :param str key: job number
    :return: json containing uuid corresponding to key, formatted as: {'jobId': <UUID>}
    :rtype: dict
    """
    global local_db

    return {"jobId": local_db.get(key, None)}


class RequestHandler(BaseHTTPRequestHandler):
    """custom request handling class"""

    def do_GET(self):
        """Custom GET response handling"""
        # calculate and apply delay
        time.sleep(random.uniform(options.delay_min, options.delay_max))

        # get the job key from the provided url path
        key = self.path.strip('/').split('/')[-1]

        # create http response header
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        # create http response body
        self.wfile.write(json.dumps(fetch_local_data(key)).encode(encoding='utf_8'))


def main(host, port, input_file, max_jobs):
    # generate local data file if necessary
    if not Path(input_file).is_file():
        generate_job_details.generate_data(max_jobs, input_file)

    # load local data into memory
    load_local_data(options.input_file)

    # start up server
    httpd = ThreadingHTTPServer((host, port), RequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    # parse program input
    parse_command_line()

    # start the webserver
    main(options.host, options.port, options.input_file, options.max_jobs)
