"""
request_data.py

This script can issue any given number of GET requests to a single endpoint to collect
a set of unique identifiers. The identifiers returned from the REST call are JOB ID's
of another system that can be tracked later. The script outputs a JSON file that contains
the list of JOB identifiers as returned from the GET request.
================================
Run this script with the following command:

    python request_data.py --num_requests=2000

where `2000` can be replaced with any positive integer
================================
Additional options can be reviewed using the following:

    python request_data.py --help
================================
This script expects a webserver to be online to receive and respond to requests
Default IP address and port are 127.0.0.1:8000

A basic webserver can be run using the following command:

    python basic_webservice.py

"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import math
import json
import requests
from tornado.options import define, options, parse_command_line

# define command-line inputs
define("num_requests", default=2000, help="number of requests to be sent", type=int)
define("output_file", default="output.json", help="output JSON file path", type=str)
define("host", default="127.0.0.1", help="server(host) address", type=str)
define("port", default=8000, help="connect to server on this port", type=int)
define("resource_path", default="", help="path to resource, appended onto base URL", type=str)
define("request_timeout", default=60, help="timeout for request (units: seconds)", type=int)
define("max_threads", default=-1, help="max threads that can be created, a value of -1 indicates that there "
                                       "should be no limit (units: seconds)", type=int)


def submit_request(job_num):
    """
    send a GET request for a given job number
    timeout guarantees function return

    :param int job_num: unique job id corresponding to a remote resource
    :return: json-encoded (dict) content of a response, if any
    :rtype: dict
    """
    # assemble url
    if options.resource_path:
        options.resource_path = options.resource_path.strip('/') + '/'
    url = "http://%s:%u/%s%u" % (options.host, options.port, options.resource_path, job_num)

    # fetch the data
    response = requests.get(url, timeout=options.request_timeout)

    # parse and return JSON response
    return response.json()


def batch_request(job_range):
    """
    Submit GET requests for each job in provided range (synchronous)

    :param Iterable job_range: iterable object (e.g. range(10))
    :return: list of dictionaries, each dictionary representing a GET response
    :rtype: list
    """
    # submit a request for each job num in range
    return [submit_request(k) for k in job_range]


def split(lrange, new_size):
    """
    Helper function to split a list into smaller ranges, each of size `n` (if possible).

    This function handles cases where length of `a` is not divisible by size `n` by
    returning as many arrays as possible of size `n` and the remainder of size `n-1`.

    There is no sorting or changing order of elements.

    :param Iterable lrange: iterable object (e.g. range(10))
    :param int new_size: desired size of each returned object
    :return: iterable of size `new_size` or `new_size - 1` (each of same type as `lrange`)
    :rtype: generator
    """
    quo, rem = divmod(len(lrange), new_size)
    for k in range(new_size):
        yield lrange[k * quo + min(k, rem):(k + 1) * quo + min(k + 1, rem)]


def request_data(*args):
    # parse program input
    parse_command_line(*args)

    # define the number of threads to use
    # this approach uses a percentage of the number of requests, up to a limit (as to not overwhelm anything)
    # note: this is just one of many ways to cap CPU and connection loads and this is definitely not the most optimal
    # (overloading of connections depends on more than just the number of requests)
    # if both client and server can handle it, num_threads should equal num_requests (this is the default behavior)
    percentage = 1  # TODO: this is a lever to optimize runtime on low-end hardware and server and should come from ML
                    # and/or actual data from testing (ideal: p = 1)
    n_thr = math.ceil(options.num_requests * percentage)
    if n_thr < options.max_threads or options.max_threads < 1:
        num_threads = n_thr
    else:
        num_threads = options.max_threads

    # generate ranges of ids each thread will be responsible for
    assignments = split(range(options.num_requests), num_threads)

    # create thread pools
    result = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # submit tasks and collect futures
        futures = (executor.submit(batch_request, r) for r in assignments)

        # process task results
        for future in as_completed(futures):
            # validate response and then add to list of results
            result.extend(v for d in future.result() if (v := d.get("jobId", None)))

    # dump results to file
    with open(options.output_file, "w") as file:
        json.dump({"jobs": result}, file, indent=4)


if __name__ == '__main__':
    # start requests
    request_data()
