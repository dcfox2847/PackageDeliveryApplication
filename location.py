

class Location:

  # O(1)
    def __init__(self, id_, address, name):
        self.id_ = id_
        self.address = address
        self.name = name
        self.dist_list = []

    # Return a string representation of the location / O(1)
    def __str__(self):
        return f'{self.id_}, {self.address}, {self.name}\n' \
            f'{self.dist_list}'


class LocationGroup:

  # O(1)
    def __init__(self):
        # The "distance_list" variable will be used to store the full information taken from the CSV file (pre-parse)
        self.distance_list = []
