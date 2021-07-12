from os.path import dirname
import sys
import unittest
import json

# Ensure that we can import the validators module
sys.path.insert(0, dirname(dirname(__file__)))

from lambda_function import (
    lambda_handler,
    get_most_suitable_link_station,
    get_distance_between_device_and_link_station,
    get_link_station_power,
    pretty_print_most_suitable_link_station,
    parse_body)

# Prepare all data required for the tests
proper_request_found = {"body": '{"device": {"coordinates": {"x": 0,"y": 0}},"linkStations": [{"coordinates": {"x": 0,"y": 0},"reach": 10}, {"coordinates": {"x": 20,"y": 20},"reach": 1}, {"coordinates": {"x": 10,"y": 0},"reach": 12}]}'}
proper_request_found_expectation = {"statusCode": 200, "headers": {"Content-Type": "application/json"},"body": "{\"finding\": \"Best link station for point 0,0 is 0,0 with power 100.0\"}"}
proper_request_found_device_coordinates = (0, 0)
proper_request_found_link_stations = [[0, 0, 10], [20, 20, 1], [10, 0, 12]]

proper_request_found_alternative = {"body": '{"device": {"coordinates": {"x": 0,"y": 0}},"linkStations": [{"coordinates": {"x": 20,"y": 20},"reach": 1}, {"coordinates": {"x": 10,"y": 0},"reach": 12}]}'}
proper_request_found_alternative_expectation = {"statusCode": 200, "headers": {"Content-Type": "application/json"},"body": "{\"finding\": \"Best link station for point 0,0 is 10,0 with power 4.0\"}"}

proper_request_not_found = {"body": '{"device": {"coordinates": {"x": 0,"y": 0}},"linkStations": [{"coordinates": {"x": 20,"y": 20},"reach": 1}]}'}
proper_request_not_found_expectation = {"statusCode": 200, "headers": {"Content-Type": "application/json"},"body": "{\"finding\": \"No link station within reach for point 0,0\"}"}

proper_device_coordinates = (12, 25)
proper_link_stations = [[10, 10, 20], [3, 3, 2], [11, 14, 20]]
proper_link_station_coordinates = (11, 14)

proper_most_suitable_link_station_expectation = (11, 14, 80.18555931250957)
proper_distance_between_device_and_link_station_expectation = 11.045361017187261

proper_distance = 5.0
proper_reach = 10.0
proper_get_link_station_power_expectation = 25.0

proper_most_suitable_link_station = (0, 0, 100)
proper_pretty_print_most_suitable_link_station_expectation = "Best link station for point 12,25 is 0,0 with power 100"

class LambdaFunctionTests(unittest.TestCase):
    # Tests lambda_handler
    def test_lambda_handler_proper_request_found(self):
        self.assertEqual(proper_request_found_expectation, lambda_handler(proper_request_found, None))

    def test_lambda_handler_proper_request_found_alternative(self):
        self.assertEqual(proper_request_found_alternative_expectation, lambda_handler(proper_request_found_alternative, None))

    def test_lambda_handler_proper_request_not_found(self):
        self.assertEqual(proper_request_not_found_expectation, lambda_handler(proper_request_not_found, None))

    # Tests get_most_suitable_link_station
    def test_get_most_suitable_link_station_proper_request(self):
        self.assertEqual(proper_most_suitable_link_station_expectation, get_most_suitable_link_station(proper_device_coordinates, proper_link_stations))

    # Tests get_distance_between_device_and_link_station
    def test_get_distance_between_device_and_link_station_proper_request(self):
        self.assertEqual(proper_distance_between_device_and_link_station_expectation,
            get_distance_between_device_and_link_station(proper_device_coordinates, proper_link_station_coordinates))

    # Tests get_link_station_power
    def test_get_link_station_power_proper_request(self):
        self.assertEqual(proper_get_link_station_power_expectation, get_link_station_power(proper_distance, proper_reach))

    # Tests pretty_print_most_suitable_link_station
    def test_pretty_print_most_suitable_link_station(self):
        self.assertEqual(proper_pretty_print_most_suitable_link_station_expectation,
            pretty_print_most_suitable_link_station(proper_device_coordinates, proper_most_suitable_link_station))

    # Tests parse_body
    def test_parse_body(self):
        parsed_body = parse_body(json.loads(proper_request_found['body']))
        self.assertEqual(proper_request_found_device_coordinates, parsed_body[0])
        self.assertEqual(proper_request_found_link_stations, parsed_body[1])

unittest.main()