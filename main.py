"""
main.py

This script times a series of HTTP GET requests

Command-line arguments are passed onto and processed by `request_data.main()`.
================================
Run this script with the following command:

    python main.py --num_requests=2000

where `2000` can be replaced with any positive integer
================================
Additional options can be reviewed using the following:

    python main.py --help
================================
This script expects a webserver to be online to receive and respond to requests
Default IP address and port are 127.0.0.1:8000

A basic webserver can be run using the following command:

    python basic_webservice.py

"""
import time

# local module
import request_data

if __name__ == "__main__":

    # start a timer
    start = time.time()

    # launch the requests
    request_data.main()

    # report the total time elapsed
    print("time elapsed to send request: %.4f" % (time.time() - start))

