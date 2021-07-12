from os.path import dirname
import sys
import unittest

# Ensure that we can import the validators module
sys.path.insert(0, dirname(dirname(__file__)))

from validators import (
    validate_most_suitable_link_station,
    validate_distance,
    validate_reach,
    validate_device_coordinates,
    validate_link_station_coordinates,
    validate_event,
    validate_body,
    validate_link_stations)

class ValidatorsTest(unittest.TestCase):
    # Tests validate_most_suitable_link_station
    def test_validate_most_suitable_link_station_none(self):
        self.assertRaises(ValueError, validate_most_suitable_link_station, None)

    def test_validate_most_suitable_link_station_not_a_tuple(self):
        self.assertRaises(ValueError, validate_most_suitable_link_station, [10, 10, 4])

    def test_validate_most_suitable_link_station_invalid_length(self):
        self.assertRaises(ValueError, validate_most_suitable_link_station, (10, 10))

    # Tests validate_distance
    def test_validate_distance_none(self):
        self.assertRaises(ValueError, validate_distance, None)

    def test_validate_distance_not_a_float(self):
        self.assertRaises(ValueError, validate_distance, 1)

    # Tests validate_reach
    def test_validate_reach_none(self):
        self.assertRaises(ValueError, validate_reach, None)

    def test_validate_reach_not_a_float(self):
        self.assertRaises(ValueError, validate_reach, 1)

    # Tests validate_link_stations
    def test_validate_link_stations_none(self):
        self.assertRaises(ValueError, validate_link_stations, None)

    def test_validate_link_stations_not_a_list(self):
        self.assertRaises(ValueError, validate_link_stations, {})

    def test_validate_link_stations_invalid_length(self):
        self.assertRaises(ValueError, validate_link_stations, [])

    def test_validate_link_station_not_a_list(self):
        self.assertRaises(ValueError, validate_link_stations, [{"key": "value"}])

    def test_validate_link_station_invalid_length(self):
        self.assertRaises(ValueError, validate_link_stations, [[3, 2, 1], [4, 3, 2, 1]])

    def test_validate_link_station_not_a_valid_x_coordinate(self):
        self.assertRaises(ValueError, validate_link_stations, [[3, 2, 1], [3.0, 2, 1]])

    def test_validate_link_station_not_a_valid_y_coordinate(self):
        self.assertRaises(ValueError, validate_link_stations, [[3, 2, 1], [3, 2.0, 1]])

    def test_validate_link_station_not_a_valid_reach(self):
        self.assertRaises(ValueError, validate_link_stations, [[3, 2, 1], [3, 2, 1.0]])

    # Tests validate_device_coordinates
    def test_validate_device_coordinates_none(self):
        self.assertRaises(ValueError, validate_device_coordinates, None)

    def test_validate_device_coordinates_not_a_tuple(self):
        self.assertRaises(ValueError, validate_device_coordinates, [10, 10])

    def test_validate_device_coordinates_invalid_length(self):
        self.assertRaises(ValueError, validate_device_coordinates, [10, 10, 10])

    def test_validate_device_coordinates_x_coordinate_not_an_int(self):
        self.assertRaises(ValueError, validate_device_coordinates, (8.0, 8))

    def test_validate_device_coordinates_y_coordinate_not_an_int(self):
        self.assertRaises(ValueError, validate_device_coordinates, (8, 8.0))

    # Tests validate_link_station_coordinates
    def test_validate_link_station_coordinates_none(self):
        self.assertRaises(ValueError, validate_link_station_coordinates, None)

    def test_validate_link_station_coordinates_not_a_tuple(self):
        self.assertRaises(ValueError, validate_link_station_coordinates, [10, 10])

    def test_validate_link_station_coordinates_invalid_length(self):
        self.assertRaises(ValueError, validate_link_station_coordinates, [10, 10, 10])

    def test_validate_link_station_coordinates_x_coordinate_not_an_int(self):
        self.assertRaises(ValueError, validate_link_station_coordinates, (8.0, 8))

    def test_validate_link_station_coordinates_y_coordinate_not_an_int(self):
        self.assertRaises(ValueError, validate_link_station_coordinates, (8, 8.0))

    # Tests validate_event
    def test_validate_event_none(self):
        self.assertRaises(ValueError, validate_event, None)

    def test_validate_event_not_a_dict(self):
        self.assertRaises(ValueError, validate_event, 14)

    # Tests validate_body
    # - tests generic
    def test_validate_body_none(self):
        self.assertRaises(ValueError, validate_body, None)

    def test_validate_body_not_a_dict(self):
        self.assertRaises(ValueError, validate_body, 14)

    # - tests device validation
    def test_validate_body_missing_device(self):
        self.assertRaises(ValueError, validate_body, {"linkStations": [{"coordinates": {"x": 0,"y": 0},"reach": 10}]})

    def test_validate_body_device_not_a_dict(self):
        self.assertRaises(ValueError, validate_body, {"device": [],"linkStations": [{"coordinates": {"x": 0,"y": 0},"reach": 10}]})

    def test_validate_body_missing_device_coordinates(self):
        self.assertRaises(ValueError, validate_body, {"device": {},"linkStations": [{"coordinates": {"x": 0,"y": 0},"reach": 10}]})

    def test_validate_body_missing_device_coordinates_not_a_dict(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": "0,0"},"linkStations": [{"coordinates": {"x": 0,"y": 0},"reach": 10}]})

    def test_validate_body_missing_x_device_coordinate(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"y": 0}},"linkStations": [{"coordinates": {"x": 0,"y": 0},"reach": 10}]})

    def test_validate_body_x_device_coordinate_not_an_int(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0.8, "y": 0}},"linkStations": [{"coordinates": {"x": 0,"y": 0},"reach": 10}]})

    def test_validate_body_missing_y_device_coordinate(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0}},"linkStations": [{"coordinates": {"x": 0,"y": 0},"reach": 10}]})

    def test_validate_body_y_device_coordinate_not_an_int(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0.8}},"linkStations": [{"coordinates": {"x": 0,"y": 0},"reach": 10}]})

    # - tests link stations validation
    def test_validate_body_missing_link_stations(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}}})

    def test_validate_body_link_stations_not_a_list(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}}, "linkStations": {}})

    def test_validate_body_missing_link_station_coordinates(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}},"linkStations": [{"reach": 10}]})

    def test_validate_body_link_station_coordinates_not_a_dict(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}},"linkStations": [{"coordinates": [], "reach": 10}]})

    def test_validate_body_missing_x_link_station_coordinate(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}},"linkStations": [{"coordinates": {"y": 0}, "reach": 10}]})

    def test_validate_body_x_link_station_coordinates_not_an_int(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}},"linkStations": [{"coordinates": {"x": 0.8, "y": 0}, "reach": 10}]})

    def test_validate_body_missing_y_link_station_coordinate(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}},"linkStations": [{"coordinates": {"x": 0}, "reach": 10}]})

    def test_validate_body_y_link_station_coordinates_not_an_int(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}},"linkStations": [{"coordinates": {"x": 0, "y": 0.7}, "reach": 10}]})

    def test_validate_body_missing_link_station_reach(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}},"linkStations": [{"coordinates": {"x": 0, "y": 0}}]})

    def test_validate_body_link_station_reach_not_an_int(self):
        self.assertRaises(ValueError, validate_body, {"device": {"coordinates": {"x": 0, "y": 0}},"linkStations": [{"coordinates": {"x": 0, "y": 0}, "reach": 10.4}]})

unittest.main()