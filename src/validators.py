def validate_most_suitable_link_station(most_suitable_link_station):
    if most_suitable_link_station is None or type(most_suitable_link_station) is not tuple or len(most_suitable_link_station) != 3:
        raise ValueError("Invalid most suitable link station specified")

def validate_distance(distance):
    if distance is None or type(distance) is not float:
        raise ValueError("Invalid distance specified")

def validate_reach(reach):
    if reach is None or type(reach) is not float:
        raise ValueError("Invalid reach specified")

def validate_link_stations(link_stations):
    if link_stations is None or type(link_stations) is not list or len(link_stations) < 1:
        raise ValueError("Invalid link stations specified")

    for link_station in link_stations:
        if type(link_station) is not list or len(link_station) != 3:
            raise ValueError("Invalid link station specified")

        if type(link_station[0]) is not int or type(link_station[1]) is not int or type(link_station[2]) is not int:
            raise ValueError("Invalid link station values specified")

def validate_device_coordinates(device_coordinates):
    if device_coordinates is None or type(device_coordinates) is not tuple or len(device_coordinates) != 2:
        raise ValueError("Invalid device coordinates specified")

    if type(device_coordinates[0]) is not int or type(device_coordinates[1]) is not int:
        raise ValueError("Invalid device coordinate specified")

def validate_link_station_coordinates(link_station_coordinates):
    if link_station_coordinates is None or type(link_station_coordinates) is not tuple or len(link_station_coordinates) != 2:
       raise ValueError("Invalid link station coordinates specified")

    if type(link_station_coordinates[0]) is not int or type(link_station_coordinates[1]) is not int:
       raise ValueError("Invalid link station coordinate specified")

def validate_event(json_object):
    if json_object is None or type(json_object) is not dict:
        raise ValueError("Invalid request")

    if 'body' not in json_object or type(json_object['body']) is not str:
        raise ValueError("No or invalid body specified")

def validate_body(json_object):
    if json_object is None or type(json_object) is not dict:
        raise ValueError("Invalid body specified")

    # Validate device
    if 'device' not in json_object or type(json_object['device']) is not dict:
        raise ValueError("Invalid device specified in the request")

    if 'coordinates' not in json_object['device'] or type(json_object['device']['coordinates']) is not dict:
        raise ValueError("Invalid device coordinates specified in the request")

    if 'x' not in json_object['device']['coordinates'] or type(json_object['device']['coordinates']['x']) is not int:
        raise ValueError("Invalid x device coordinate specified in the request")

    if 'y' not in json_object['device']['coordinates'] or type(json_object['device']['coordinates']['y']) is not int:
        raise ValueError("Invalid y device coordinate specified in the request")

    # Validate link stations
    if 'linkStations' not in json_object or type(json_object['linkStations']) is not list:
        raise ValueError("No valid link stations list specified in the request")

    for link_station in json_object['linkStations']:
        if type(link_station) is not dict:
            raise ValueError("Invalid link station specified in the request")

        if 'coordinates' not in link_station or type(link_station['coordinates']) is not dict:
            raise ValueError("Invalid link station coordinates specified in the request")

        if 'x' not in link_station['coordinates'] or type(link_station['coordinates']['x']) is not int:
            raise ValueError("Invalid x link station coordinate specified in the request")

        if 'y' not in link_station['coordinates'] or type(link_station['coordinates']['y']) is not int:
            raise ValueError("Invalid y link station coordinate specified in the request")

        if 'reach' not in link_station or type(link_station['reach']) is not int:
            raise ValueError("Invalid link station reach specified in the request")