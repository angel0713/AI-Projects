'''
Author: Angel Mendez
Professor: Kate Nguyen
Course: CECS 451 - Artificial Intelligence
Assignment #1: A* Algorithm
'''

import sys
from math import asin, cos, radians, sin, sqrt
from queue import PriorityQueue
from typing import Dict, Any, Tuple

r = 3_958.8  # radius of the earth in miles


# Perform the A* algorithm to search for the optimal pathway
def a_star_function(s, t, map, coordinates) -> [list, float]:
    # Initialize an empty list
    open_list = []
    # Create a tuple with initial values
    initial = (0, s, [s])
    # Append the initial element to open_list
    open_list.append(initial)
    while open_list:
        # Calculate the cost using a lambda function
        lambda_function = lambda x: x[0] + haversine_function(coordinates[t], coordinates[x[1]])
        # Find the minimum element in open_list using the cost_function
        minimum = min(open_list, key=lambda_function)
        # After we find the next minimum element we will break it down into 3 parts
        # print("this is min element", min_element)
        total_cost, node, path = minimum

        open_list.remove((total_cost, node, path))  # If we haven't returned a path then we need to start removing
        # already explored
        # cities with .remove((g,current,path))
        # Then we will continue to
        for neighbor in map[node]:
            # if we find that the neighbor city is not in the path then we'll add the neighboring city
            # We'll also update the cost and path
            if neighbor not in path:
                add_cost = total_cost + map[node][neighbor]
                add_path = path + [neighbor]
                open_list.append((add_cost, neighbor, add_path))
                print("here is open_list in the a_star_function", open_list)

        # if the current city is equal to the final destination we can return the path and distance to get there
        if node == t:
            print("path: ", path)
            print("total_cost", total_cost)
            return path, total_cost
    return None  # if we do not get a path we will just return an empty list for the path and a distance of 0


# A function that calculates the haversine distance between two coordinates
def haversine_function(c1, c2) -> float:
    # Set my coordinates (in degrees)
    lon1, lat1 = c1
    lon2, lat2 = c2

    # Convert them to radians so we can apply haversine function
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)

    # Get difference between the longitude and latitude values
    difference_lon = lon2 - lon1
    difference_lat = lat2 - lat1

    # execute haversine formula and return the mileage value
    a = sin(difference_lat / 2) ** 2
    a += cos(lat1) * cos(lat2) * sin(difference_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    print("haversine_function", r*c)
    # Calculate the final and return the Haversine distance
    return r * c


# We must read the coordinates from a 'coordinates.txt' file where the values are stored such as:
# 'SanJose:(37.38305013,-121.8734782)'
# We must parse through the text file in order to store the coordinate tuple and pair it with the city name using
# Python's dictionary functionalities
def read_coordinates(name) -> dict[Any, tuple[float, float]]:  # Need coordinates from 'coordinates.txt'
    coordinates = {}  # declare dictionary to store our coords for the cities

    with open(name, 'r') as name:  # Using the open function we'll read from the file (name from argument entry)
        lines = name.readlines()  # Read the lines and store them in 'parse'
    parse = lines
    for p in parse:  # Create for loop to parse through the file
        city, coordinate = p.strip().split(
            ':')  # We need to split the city and coordinate using ':' into their own respective variables
        # Split the 'coordinate' string into a list using ',' as the splitter
        # remove the last and first element from the coordinate as it doesn't fit in our data structure format
        coord_values = coordinate[1:-1].split(',')

        # Convert the list to floats for latitude and longitude
        latitude = float(coord_values[0])
        longitude = float(coord_values[1])

        coordinates[city] = (longitude, latitude)  # set dictionary definition of the city to a tuple of the
        # longitude and latitude
        print("Coordinates returned in read_coordinates)", coordinates)
    return coordinates  # return the dictionary of coordinates


# similar to the read_coordinates() function we will parse through a text file (map.txt) in order to gain
# a sort of map that we can traverse and manipulate in this python program
def read_map(name) -> dict[Any, dict[Any, Any]]:
    # just like read_coordinates() we will open/read the file using open
    # then create a dictionary to save values in
    map = {}
    with open(name, 'r') as name:
        lines = name.readlines()
    parsed = lines

    for p in parsed:
        city, nearby_city = p.strip().split('-')  # strip the text file into city (the first one) and neighbor values
        map[city] = {}
        for nearby_city in nearby_city.split(
                ','):  # then once we have the neighbor value in python we need to split the values using ',' as the
            # deliminator
            city2, d = nearby_city.split(
                '(')  # we need to gain the value of city2 and the distance value and save them to variables
            # we need to get rid of the ')' and convert the string to a float (distance)
            temp = float(d[:-1])
            map[city][city2] = temp
    print("map", map)
    return map  # return the full neighbor list of each city


if __name__ == '__main__':
    # Raise an error if not enough arguments has been entered by the user
    if len(sys.argv) != 3 or sys.argv[1] is None or sys.argv[2] is None:
        raise ValueError("Error: Please ensure you enter 3 arguments such as 'python a-star.py SanFrancisco LongBeach")
    # elif s == t:
    #     raise ValueError("Error: You entered the same city for the start and end cities")
    else:
        # take user's input from CLI
        s = sys.argv[1]
        t = sys.argv[2]

    if s == t:
        raise ValueError("Error: You entered the same city for the start and end cities")

    # Grab values from the provided text files
    map = read_map("map.txt")
    print("map", map)
    # print("Here is map", map)
    coordinates = read_coordinates("coordinates.txt")
    # print("Here is coordinates", coordinates)
    print("coordinates", coordinates)

    if s not in map:
        raise ValueError("Error: You did not enter a valid city for the start city")
    elif t not in map:
        raise ValueError("Error: You did not enter a valid city for the final destination")

    # graph the pathway and the total_distance_cost from the a_star() function

    complete_path, distance = a_star_function(s, t, map, coordinates)

    # print (pathway)
    if complete_path is None:
        print("There is no path")

    # Finally, print out the necessary output as the assignment requirements state
    print(f"from city: {s}\nto city: {t}")
    print(f'Best Route:', end=' ')
    # print out the results in the format that is in our project requirements
    for r in complete_path:
        if r == complete_path[len(complete_path) - 1]:
            print(r)
            break
        else:
            print(r + ' - ', end='')
    # print('\b\b\b\b\b\b\b')
    print(f'Total distance: {distance:.2f} Miles')
