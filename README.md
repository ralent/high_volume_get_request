# High Volume Read Request Strategies

This tool can issue any given number of GET requests to a single endpoint to collect
a set of unique identifiers. The identifiers returned from the REST call are JOB Id's
of another system that can be tracked later. The script outputs a JSON file that contains
the list of JOB identifiers as returned from the GET request.

## Purpose

The purpose of this tool is to demonstrate one way to quickly send a high volume of requests to a single endpoint. This strategy relies on multi-threading, and specifically thread pools to do so. The scope of this effort is limited to the client's request handling and, consequently, it is assumed that the endpoint/server is optimized for handling high volume simultaneous read requests (e.g. load-balancing). One particular challenge this tool attempts to tackle is highly varying request response times (e.g. 1 - 10 response delays).

## Getting Started

### Dependencies

This tool requires Python 3.

A requirements file is included in the repo and can be installed using the following command:

    pip install -r requirements.txt

Alternatively, the dependencies can be installed with the following command:

    pip install tornado requests

### Executing program

All code can be run in either Windows or Linux.

#### Starting a web server

Before making requests a webserver needs to be running and able to response to GET requests. To make testing easy, a simple tornado-based HTTP webserver is included and can be run using the following command:

    python basic_webservice.py

Note: this command will block a terminal/shell until forcefully terminated using a KeyboardInterrupt (`Ctrl+C`)

The default IP address and port for the server is: **127.0.0.1:8000**

#### Sending requests

Once you have a web server set up, you can send requests with the following command:

    python request_data.py

this command will generate a JSON file in the current working directory (default name: `output.json`) of the following format:

```
{
    'jobs': [<uuid1>, <uuid>, ...]
}
```

#### Validation

Data can be validated, after running `request_data.py` using the following command

    python validate.py

If data validates successfully, `validate.py` will print to stdout: `SUCCESS: data successfully fetched from server`

This function compares the output json file and compares its content to the original data file loaded into the web server

## Help

```commandline
Usage: python request_data.py [OPTIONS]

Options:

  --help                           show this help information
  --host                           server(host) address (default: "127.0.0.1")
  --max-threads                    max threads that can be created, a value of -1 indicates that 
                                   there should be no limit (units: seconds) (default -1)           
  --num-requests                   number of requests to be sent (default: 2000)
  --output-file                    output JSON file path (default: "output.json")
  --port                           connect to server on this port (default: 8000)
  --request_time                   timeout for request (units: seconds) (default: 60)
  --resource-path                  path to resource, appended onto base URL (default: None)   
```

```commandline
Usage: python http_webserver.py [OPTIONS]

Options:

  --help                           show this help information
  --delay-max                      maximum artificial delay for GET requests (units: seconds) (default: 10)
  --delay-min                      minimum artificial delay for GET requests (units: seconds) (default: 1)
  --host                           bind server to this host (e.g. 127.0.0.1) (default "127.0.0.1")
  --input-file                     file path to JSON data that will be fetched (default: "jobDetails.json")
  --max-jobs                       max number of jobs (default: 2000)
  --port                           connect to server on this port (default: 8000)
```

```commandline
Usage: python validate.py [OPTIONS]

Options:

  --help                           show this help information
  --input-file                     file path to JSON data that will be fetched (default: "jobDetails.json")
  --output-file                    output JSON file path (default: "output.json")

```

## Version History

* 0.1
    * Initial Release

