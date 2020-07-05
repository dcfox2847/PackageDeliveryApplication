from package import *
from graph import *
from datetime import *


class Truck:

    """
    The truck class will need variables for which driver is in the truck, information for the time in regards to
    where the truck is, and when it will arrive, max package capacity, and a "ready" status for if the truck is ready
    to deliver all of its packages.
    """

    # O(1)
    def __init__(self, id_=None, driver=None, miles_driven=0, hub_node=None,
                 ready_status=False, current_location="HUB", next_location=None, retire_truck=False):
        self.id = id_
        self.driver = driver
        self.cargo_list = []
        self.delivered_packages = []
        self.departure_time = None
        self.departure_seconds = None
        self.miles_driven = miles_driven
        self.hub_node = hub_node
        self.ready_status = ready_status
        self.current_location = current_location
        self.next_location = next_location
        self.current_location_information = None
        self.next_location_information = None
        self.dist_list = None
        self.retire_truck = retire_truck
        self.speed = 18  # This is the time in MPH

    # Method for loading the packages onto the truck / O(n)
    def load_truck(self, package_list):
        for x in package_list:
            self.cargo_list.append(x)

    # Method for getting the information on your next location / O(n)
    def next_location_info(self, next_package, location_list):
        address = next_package
        for y in location_list:
            if y.id_ == address:
                self.next_location_information = y

    # Look for late delivered package /
    # def get_late_package(self, cargo_list):
    #     if cargo_list

    # Method for getting the information on your next location / O(n^2)
    def find_closest_location(self, package_list, location_list, graph):
        distance_id_list = []
        smallest_value = float('inf')
        smallest_index = int()
        for x in package_list:
            package_add = x.address
            for y in location_list:
                if y.name == package_add:
                    distance_id_list.append(int(y.id_))
        for x in distance_id_list:
            new_value = float(graph.edge_weights[(x, self.current_location_information.id)])
            if new_value < smallest_value:
                smallest_value = new_value
                smallest_index = int(x)
        self.next_location = smallest_index

    # Set id number as 'next_location' / O(1)
    def set_next_location(self, location_id):
        self.next_location = location_id

    # After package delivery, set the current location to what was the "next_location" / O(1)
    def set_new_current_location(self):
        self.current_location = self.next_location

    # Build method for delivering a package (remove from the cargo list, and add to delivered list) O(n^2)
    def deliver_packages(self, miles_driven):
        packages_to_deliver = []
        package_info_list = []
        for x in self.cargo_list:
            if x.address == self.next_location_information.name:
                packages_to_deliver.append(x)
        for x in self.cargo_list:
            for y in packages_to_deliver:
                if x.id == y.id:
                    package_info_list.append(x)
        for y in self.cargo_list:
            for i in package_info_list:
                if y == i:
                    y.miles_driven = round(miles_driven, 2)
                    self.cargo_list.remove(y)
                    self.delivered_packages.append(y)
                    item = self.delivered_packages.index(y)
                    self.delivered_packages[item].status = "DELIVERED"

    # Build the method for converting the time to a string / O(1)
    def get_seconds(self, t):
        list = t.split(':')
        hours = list[0]
        minutes = list[1]
        seconds = list[2]
        total = (int(hours) * 3600 + int(minutes) * 60 + int(seconds))
        return total
