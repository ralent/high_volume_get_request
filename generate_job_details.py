"""
generate_data.py

this script generates a JSON file with arbitrary data that can feed
into a dummy webserver in order to respond to requests

this script relies on uuid4() so each time it runs, it will generate random data
"""
import json
import uuid


def generate_data(max_jobs, output_file):
    """

    :param max_jobs:
    :param output_file:
    :return:
    """
    # create a list of job ids, these will be simple, incrementing positive integers
    job_num = tuple(range(max_jobs))

    # create a list of unique identifiers that will correlate to the job ids above
    job_uid = (str(uuid.uuid4()) for _ in range(max_jobs))

    # combine lists into a dictionary
    job_details = dict(zip(job_num, job_uid))

    # dump to file
    with open(output_file, "w") as file:
        json.dump(job_details, file, indent=4)


