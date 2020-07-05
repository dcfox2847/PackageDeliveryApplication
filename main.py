"""
Daniel Fox
#000879930
WGU -> Data Structures and Algorithms 2 -> C950
"""

from graph import Vertex, Graph
from package import *
from hashtable import *
from location import *
from truck import *
import datetime
import time
import csv
import os
import operator


# Declare the variables that will be used throughout the program
package_group = PackageGroup()
location_group = LocationGroup()
package_hash_table = ChainingHashTable()
graph = Graph()
truck_1_graph = Graph()
truck_2_graph = Graph()
truck_3_graph = Graph()
truck_1 = Truck()
truck_2 = Truck()
truck_3 = Truck()
truck_group = [truck_1, truck_2, truck_3]
total_distance_all_trucks = 0
all_delivered_packages = []
truck_1.departure_time = '08:00:00'
truck_2.departure_time = '09:10:00'
truck_3.departure_time = '09:47:00'


"""
Created functions necessary for program operation
"""


# Create a clear screen function
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Function to get the current location of a given "Truck" object / O(1)
def get_location_information(truck):
    curr_spot = truck.current_location
    if curr_spot == "HUB":
        truck.current_location = 1
        truck.current_location_information = package_group.package_list[1]
    else:
        truck.current_location_information = package_group.package_list[truck.current_location]


""" End main algorithm and related functions"""

# Read in package.csv and create package objects.
# The package objects are then stored in the 'package_group' object to be further sorted and parsed / O(n)
with open('package.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        package_key = package.id
        package_hash_table.insert(package_key, package)
    package_hash_table.return_all_items(package_group.package_list)
    file.close()

# Read in distance.csv and create a distance matrix
# Individual location objects are created, then that information is sent over to the location_group object / O(n^2)
with open('distances.csv') as file:
    reader = csv.reader(file)
    count = 0
    for row in reader:
        count = count + 1
        location = Location(count, row[0], row[1])
        for x in row[2:]:
            if x == '' or x == '0':
                continue
            else:
                location.dist_list.append(x)
        location_group.distance_list.append(location)
    file.close()

# Create the vertices from the imported CSV data, and then insert that data into the graph object. / O(n)
for x in location_group.distance_list:
    x = Vertex(x.id_, x)
    graph.add_vertex(x)

# Create and append the 'node_list' variable / O(n)
node_list = []
for x in graph.adjacency_list:
    node_list.append(x)

# Set the current location to the index of the 'l' variable in the previously created 'node_list'.
# Then set the 'curr_dist' variable to the index of the 'i' in 'dist_list'. / O(n^2)
for l in node_list:
    curr_location = int(node_list.index(l))
    for i in l.location.dist_list:
        curr_dist = l.location.dist_list.index(i)
        if i is not '' or i is not '0':
            try:
                graph.add_undirected_edge(node_list[curr_dist], node_list[curr_location], float(i))
            except IndexError:
                continue


# This is all error correction information.... it checks to see if all tuples have been added using the
# "add_undirected_edge" method. If not, it uses error checking to make sure that everything is added that needs to be. / O(n^2)
for x in range(1, 28):
    for i in range(x+1, 28):
        try:
            try:
                graph.edge_weights[(x, i)]
            except KeyError:
                first_index = node_list[x]
                first_dist_index = node_list.index(x)
                second_index = node_list[i]
                graph.add_undirected_edge(first_index, second_index, location_group.distance_list[i].dist_list[x])
        except IndexError:
            continue
graph.add_undirected_edge(node_list[21], node_list[14], float(7.4))
graph.add_undirected_edge(node_list[21], node_list[15], float(6.9))
graph.add_undirected_edge(node_list[20], node_list[12], float(8.5))
graph.add_undirected_edge(node_list[20], node_list[15], float(4.9))
graph.add_undirected_edge(node_list[21], node_list[21], float(0.0))
graph.add_undirected_edge(node_list[21], node_list[17], float(5.0))
graph.add_undirected_edge(node_list[21], node_list[12], float(10.3))
graph.add_undirected_edge(node_list[17], node_list[12], float(5.9))
graph.add_undirected_edge(node_list[19], node_list[4], float(6.5))
graph.add_undirected_edge(node_list[18], node_list[2], float(5))
graph.add_undirected_edge(node_list[18], node_list[12], float(5.4))
graph.add_undirected_edge(node_list[18], node_list[15], float(1.7))
graph.add_undirected_edge(node_list[19], node_list[12], float(1))
graph.add_undirected_edge(node_list[19], node_list[19], float(0))
graph.add_undirected_edge(node_list[15], node_list[12], float(6.6))
graph.add_undirected_edge(node_list[15], node_list[6], float(5.8))
graph.add_undirected_edge(node_list[25], node_list[17], float(5.1))
graph.add_undirected_edge(node_list[22], node_list[8], float(7.8))
graph.add_undirected_edge(node_list[22], node_list[12], float(10.3))
graph.add_undirected_edge(node_list[26], node_list[12], float(14.1))
graph.add_undirected_edge(node_list[23], node_list[12], float(4.4))
graph.add_undirected_edge(node_list[25], node_list[8], float(2.8))
graph.add_undirected_edge(node_list[25], node_list[12], float(2.8))
graph.add_undirected_edge(node_list[16], node_list[8], float(7.2))
graph.add_undirected_edge(node_list[16], node_list[12], float(7.2))
graph.add_undirected_edge(node_list[14], node_list[12], float(2.6))
graph.add_undirected_edge(node_list[24], node_list[8], float(9.5))
graph.add_undirected_edge(node_list[24], node_list[15], float(5.9))


# The Methods for loading the trucks with the pre-sorted packages:
package_group.pre_sort(package_group.package_list)
truck_1.load_truck(package_group.list_1)
truck_2.load_truck(package_group.list_2)
truck_3.load_truck(package_group.list_3)


# Deliver packages and get mileage for truck 1 / O(n^2)
while truck_1.cargo_list:
    get_location_information(truck_1)
    truck_1.find_closest_location(truck_1.cargo_list, location_group.distance_list, graph)
    truck_1.next_location_info(truck_1.next_location, location_group.distance_list)
    ''' ^ The above code finds the next location^ '''
    truck_1.miles_driven = truck_1.miles_driven + graph.edge_weights[(truck_1.current_location_information.id, truck_1.next_location)]
    # The truck drives the miles calculated above ^ and then "delivers" the packages
    # Below, you call the method to deliver the packages (remove from cargo_list, and add to delivered_list)
    truck_1.deliver_packages(truck_1.miles_driven)
    # Set the 'current_location" (which is an integer id) to the "next_location" (also an integer id)
    truck_1.set_new_current_location()

# Deliver packages and get mileage for truck 2 / O(n^2)
while truck_2.cargo_list:
    get_location_information(truck_2)
    truck_2.find_closest_location(truck_2.cargo_list, location_group.distance_list, graph)
    truck_2.next_location_info(truck_2.next_location, location_group.distance_list)
    ''' ^ The above code finds the next location^ '''
    truck_2.miles_driven = truck_2.miles_driven + graph.edge_weights[(truck_2.current_location_information.id,
                                                                      truck_2.next_location)]
    # The truck drives the miles calculated above ^ and then "delivers" the packages
    # Below, you call the method to deliver the packages (remove from cargo_list, and add to delivered_list)
    truck_2.deliver_packages(truck_2.miles_driven)
    # Set the 'current_location" (which is an integer id) to the "next_location" (also an integer id)
    truck_2.set_new_current_location()

# Deliver packages and get mileage for truck 3 O(n^2)
while truck_3.cargo_list:
    get_location_information(truck_3)
    truck_3.find_closest_location(truck_3.cargo_list, location_group.distance_list, graph)
    truck_3.next_location_info(truck_3.next_location, location_group.distance_list)
    ''' ^ The above code finds the next location^ '''
    truck_3.miles_driven = float(truck_3.miles_driven) + float(graph.edge_weights[(truck_3.current_location_information.id,
                                                                      truck_3.next_location)])
    # The truck drives the miles calculated above ^ and then "delivers" the packages
    # Below, you call the method to deliver the packages (remove from cargo_list, and add to delivered_list)
    truck_3.deliver_packages(truck_3.miles_driven)
    # Set the 'current_location" (which is an integer id) to the "next_location" (also an integer id)
    truck_3.set_new_current_location()

# To give the total miles given, add each of the trucks (truck_1, 2, and 3) miles_driven to be displayed in the final program

total_distance_all_trucks = truck_1.miles_driven + truck_2.miles_driven + truck_3.miles_driven



# THIS IS THE BASIS FOR FINDING THE TIME DRIVEN BY EACH VEHICLE!!!!

# You have created datetime objects for the "time" variable in the truck object. Convert this time to seconds, add the "arrival_time" of each package on the truck.
# After that, you convert the original time, with the added seconds, back to the standard time. You can display the time from here.
# Explanation: Take 'departure time' converted to seconds, iterate through the  ''arrival_time"  and add it to the 'departure_time', then return it as a new VARIABLE in the package class
# I.e. 8000 seconds + 350 seconds = 8350 seconds 
# Then CONVERT the 8350 seconds to a string  in the format of H:M:S (ex. '02:11:06')
# us this to convert : str(datetime.timedelta(seconds=8350)) -> '0:11:06'
# Use the 'get_seconds' method to convert the departure time to seconds / O(1)
for x in truck_group:
    x.departure_seconds = x.get_seconds(x.departure_time)

# Search through the list comprised of all available trucks, then look at the time of each delivered package
# Do the converstion to get the final "arrival" time of each package / O(n^2)
for x in truck_group:
    for i in x.delivered_packages:
        i.arrival_time = round(float(i.miles_driven / x.speed), 3)
        i.arrival_time = round(i.arrival_time * 3600, 2)
        i.final_seconds = i.arrival_time + x.departure_seconds
        i.final_arrival = str(datetime.timedelta(seconds=round(i.final_seconds)))

# BEGIN THE MAIN APPLICATION SECTION OF THE CODE!!!!
# This is where all of the user interactivity will be programmed into the application
# Complexity: O(n^2)
program_continue = True


print("Welcome to the WGUPS parcel tracking program.")
print("All packages have been successfully delivered for the day!")
while program_continue is True:
    print("\n")
    print("Enter 'miles' to see the total number of miles our vehicles drove today.")
    print("Enter 'lookup' to find information on a package based on the package ID.")
    print("Enter 'time' to enter a time, and see the status of all packages during that time.")
    print("Enter 'exit' to quit the program.")
    user_input = input(f'Please tell us what you would like to do today?  ')
    if user_input == 'miles':
        print(f'The total miles driven by our trucks today was {total_distance_all_trucks} miles.\n')
        input("Press any key to continue....")
        clear()
    elif user_input == 'lookup':
        try:
            package_info = int(input("Please enter the ID number of the package you would like to look up: "))
            for x in truck_group:
                for i in x.delivered_packages:
                    if i.id == package_info:
                        print(f'Package ID {i.id} was delivered successfully to {i.address} {i.city}, {i.state} at'
                              f' {i.final_arrival}. The deadline was {i.deadline}. The weight of the package was'
                              f' {i.weight} pounds upon intake.\n')
        except ValueError:
            print("Invalid Entry")
            continue
        input("Press any key to continue....")
        clear()
    elif user_input == 'time':
        user_time =  input('Please enter a time in the format HH:MM:SS: ')
        print(f'The time entered was {user_time}')
        try:
            user_time = truck_1.get_seconds(user_time)
            for x in truck_group:
                for i in x.delivered_packages:
                    if user_time < i.final_seconds and user_time < x.departure_seconds:
                        print(f'Package ID {i.id} is at the Hub waiting to be delivered.')
                    elif user_time < i.final_seconds and user_time >= x.departure_seconds:
                        print(f'Package ID {i.id} is en route to be delivered to {i.address} {i.city}, {i.state}.')
                    elif user_time >= i.final_seconds and user_time >= x.departure_seconds:
                        print(f'Package ID {i.id} has been delivered to {i.address} {i.city}, {i.state} at'
                              f' {i.final_arrival}.')
        except IndexError:
            print("That is not the proper format.")
            continue
        except ValueError:
            print("That is not the proper time format.")
            continue
        input("Press any key to continue....")
        clear()
    elif user_input == 'exit':
        exit()
    else:
        print("That was not a valid option....\n")
        input("Press any key to continue....")
        clear()
