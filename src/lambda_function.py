import json
import math

from validators import (
    validate_most_suitable_link_station,
    validate_distance,
    validate_reach,
    validate_device_coordinates,
    validate_link_station_coordinates,
    validate_event,
    validate_body,
    validate_link_stations)

def lambda_handler(event, context):
    # Validate the incoming event
    validate_event(event)

    # Parse and validate the body
    parsed_body = parse_body(json.loads(event['body']))

    # Get the device coordinates and link stations
    device_coordinates = parsed_body[0]
    link_stations = parsed_body[1]

    # Find the most suitable link station
    most_suitable_link_station = get_most_suitable_link_station(device_coordinates, link_stations)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "finding": pretty_print_most_suitable_link_station(device_coordinates, most_suitable_link_station)
        })
    }

def get_most_suitable_link_station(device_coordinates, link_stations):
    # Validate device coordinates
    validate_device_coordinates(device_coordinates)

    # Validate link stations
    validate_link_stations(link_stations)

    # Set the default value for the most suitable link station
    most_suitable_link_station = (0, 0, 0.0)

    for link_station in link_stations:
        # calculate device's distance
        distance = get_distance_between_device_and_link_station(device_coordinates, (link_station[0], link_station[1]))

        # calculate power per link station
        power = get_link_station_power(float(distance), float(link_station[2]))

        # compare link stations based on power
        if power > most_suitable_link_station[2]:
            most_suitable_link_station = (link_station[0], link_station[1], power)

    return most_suitable_link_station

def get_distance_between_device_and_link_station(device_coordinates, link_station_coordinates):
    # Validate device coordinates
    validate_device_coordinates(device_coordinates)

    # Validate link station coordinates
    validate_link_station_coordinates(link_station_coordinates)

    # Calculate the distance on the x and y axis
    distance_x = abs(device_coordinates[0] - link_station_coordinates[0])
    distance_y = abs(device_coordinates[1] - link_station_coordinates[1])

    # Calculate the distance based on the Pythagoras theorem (assuming that the distance is a straight line)
    return math.sqrt(pow(distance_x, 2) + pow(distance_y, 2))

def get_link_station_power(distance, reach):
    # Validate distance and reach
    validate_distance(distance)
    validate_reach(reach)

    power = 0.0

    # Only calculate power when the reach is greater than the distance
    if reach > distance:
        power = pow((reach - distance), 2)

    return power

def pretty_print_most_suitable_link_station(device_coordinates, most_suitable_link_station):
    # Validate device coordinates
    validate_device_coordinates(device_coordinates)

    # Validate the most suitable link station
    validate_most_suitable_link_station(most_suitable_link_station)

    pretty_response = ""

    if most_suitable_link_station[2] > 0.0:
        pretty_response = "Best link station for point {},{} is {},{} with power {}".format(
            device_coordinates[0],
            device_coordinates[1],
            most_suitable_link_station[0],
            most_suitable_link_station[1],
            most_suitable_link_station[2]
        )
    else:
        pretty_response = "No link station within reach for point {},{}".format(device_coordinates[0], device_coordinates[1])

    return pretty_response

def parse_body(json_object):
    # Validate that the request is complete and specified properly
    validate_body(json_object)

    # Get the device coordinates as a tuple (since the problem statement showed the device points as tuples)
    device_coordinates = (json_object['device']['coordinates']['x'], json_object['device']['coordinates']['y'])

    link_stations = []

    # Get the link stations as a list (since the problem statement showed the link stations as lists)
    for link_station in json_object['linkStations']:
        link_stations.append([
            link_station['coordinates']['x'],
            link_station['coordinates']['y'],
            link_station['reach']
        ])

    return device_coordinates, link_stations