"""
basic_webservice.py

Start a simple webservice to supports GET requests
"""

import asyncio
import json
from abc import ABC
from pathlib import Path
import random
from tornado import web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

# local module
import generate_job_details

# define command-line inputs
define("port", default=8000, help="run on the given port", type=int)
define("max_jobs", default=2000, help="max number of jobs", type=int)
define("delay_min", default=1, help="minimum artificial delay for GET requests (units: seconds)", type=float)
define("delay_max", default=10, help="maximum artificial delay for GET requests (units: seconds)", type=float)
define("input_file", default="jobDetails.json", help="file path to JSON data that will be fetched", type=str)
define("resource_path", default="getjobdetails/", help="url suffix where data will be available", type=str)


class GetHandler(web.RequestHandler, ABC):
    """
    GET request handler
    """

    def initialize(self, data):
        """Called before each get request. Used to provide data to custom get handling function"""
        self.data = data

    async def get(self, key):
        """
        Custom GET response handler
        With a give job number, respond with the corresponding UUID in the following format: {'jobId': <UUID>}

        :param str key: job number
        """
        # calculate and apply delay
        delay = random.uniform(options.delay_min, options.delay_max)

        if delay > 0:
            await asyncio.sleep(delay)

        # return with job info
        self.write(json.dumps({"jobId": self.data.get(key, None)}))

        await self.flush()


def main():
    # parse program input
    parse_command_line()

    # generate data file if necessary
    if not Path(options.input_file).is_file():
        generate_job_details.generate_data(options.max_jobs, options.input_file)

    # load job details from file
    with open(options.input_file) as f:
        data = json.load(f)

    # start-up webserver
    application = web.Application([("/" + options.resource_path.strip("/") + "/(.*)", GetHandler, dict(data=data))])
    http_server = HTTPServer(application)
    http_server.listen(options.port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
