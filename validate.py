"""
The purpose of this script is to validate test data to true/original data
"""
import json
from tornado.options import define, options, parse_command_line

define("input_file", default="jobDetails.json", help="file path to JSON data that will be fetched", type=str)
define("output_file", default="output.json", help="output JSON file path", type=str)


def validate_data(test_jsonfile, true_jsonfile):
    """
    Validate the data downloaded, comparing directly against the server data

    :param test_jsonfile: path to the JSON file with test data, must be in format: {'jobs': [<job uuids>]}
    :param true_jsonfile: path to the JSON file with true data, must be in format: {'0': [<uuid0>], '1': [<uuid1>],...}
    :return: true if data matches
    :rtype: bool
    """
    # get data that we intend to validate
    with open(test_jsonfile, "r") as f:
        test_data_raw = json.load(f)

        # format the data
        test_data = test_data_raw.get("jobs", []).sort()

    # get data that we know to be correct
    with open(true_jsonfile, "r") as f:
        true_data_raw = json.load(f)

        # format the data
        true_data = list(true_data_raw.values()).sort()

    # compare the data
    return test_data == true_data


if __name__ == '__main__':
    # parse program input
    parse_command_line()

    # validate data and report result
    if validate_data(options.output_file, options.input_file):
        print("SUCCESS: data successfully fetched from server")
    else:
        print("FAILED: something went wrong with the request")
