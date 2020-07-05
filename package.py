
class Package:
    def __init__(self, id_, address, city, state, zip_code, deadline, weight, special_instructions):
        self.id = int(id_)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.special_instructions = special_instructions
        self.miles_driven = float(0)
        self.arrival_time = None
        self.final_seconds = None
        self.final_arrival = None
        self.status = None
        self.delayed = None
        self.delivered_with = []

        # Check to see if the package has a delivery constraint of EOD, or AM, then parse the numbers out of the time  / O(1)
        if 'AM' in deadline:
            self.deadline = int(deadline.replace(' AM', '').replace(':', ''))
        elif 'EOD' in deadline:
            self.deadline = None

        # Check to see if there is a delay in the package. If so parse the time from the comment for the constraint / O(1)
        instructions = self.special_instructions.upper()
        if 'DELAYED' in instructions:
            self.delayed = True
            self.status = "NOT_YET_ARRIVED"
            pos = instructions.index(':') - 1
            new_string = instructions[pos:]
            formatted_string = int(new_string.replace(' AM', '').replace(':', ''))
            self.arrival_time = formatted_string
        else:
            self.delayed = False
            self.arrival_time = 800
            self.status = "AT_HUB"

        # Check to see if packages need to be delivered with other packages. If so, create a list of packages / O(n)
        if "MUST BE DELIVERED WITH" in instructions:
            instructions = instructions.replace(',', '')
            group_instructions = instructions.split()
            for word in group_instructions:
                if word.isdigit():
                    self.delivered_with.append(int(word))

        # Check to see if a package has the wrong address / O(1)
        if "WRONG ADDRESS LISTED" in instructions:
            self.delayed = True
            self.status = "AWAITING_ADDRESS_CHANGE"

    # Change the string method so that you can check to see that all of the attributes of the object
    # are being displayed correctly. / O(1)

    def __str__(self):
        return f'{self.id}, {self.address}, {self.city}, {self.state}, {self.zip_code}, {self.deadline}, ' \
            f'{self.weight}, {self.special_instructions}, {self.arrival_time}, {self.delayed}, {self.status},' \
            f'{self.delivered_with}'


class PackageGroup:

    # Create the package group class instance
    # This class instance will have 3 separate lists of packages. Each list will go to a specific truck. / O(1)
    def __init__(self):
        self.max_amount = 16
        self.package_list = []
        self.list_1 = []
        self.list_2 = []
        self.list_3 = []
        self.loaded_packages = []

    # Create an algorithm to pre-sort the packages from the list / O(n^2)

    def pre_sort(self, package_list):
        self.deliver_with(package_list)
        self.delayed_package(package_list)
        self.specific_truck(package_list)
        self.package_deadline(package_list)
        self.greed_load(package_list)

    # Check to see if the packages are required to be delivered together, the put them on same truck / O(n)    
    def deliver_with(self, package_list):
        pack_group = []
        for package in package_list:
            if package not in self.loaded_packages:
                if len(package.delivered_with) > 0:
                    pack_group.append(package.id)
                    for x in package.delivered_with:
                        if x not in pack_group:
                            pack_group.append(x)
        for package in package_list:
            for x in pack_group:
                if x == package.id:
                    self.list_1.append(package)
                    self.loaded_packages.append(package)

    # Check to see if a package has a status of "AWAITING_ADDRESS_CHANGE" or "NOT_YET_ARRIVED"
    # If so add these packages to the third trucks list / O(n)
    def delayed_package(self, package_list):
        for package in package_list:
            if package not in self.loaded_packages:
                if package.status == "AWAITING_ADDRESS_CHANGE" or package.status == "NOT_YET_ARRIVED":
                    self.list_3.append(package)
                    self.loaded_packages.append(package)

    # Check to see if a package has to be on a specific truck / O(n)
    def specific_truck(self, package_list):
        for package in package_list:
            if package in self.loaded_packages:
                continue
            else:
                if "truck 2" in package.special_instructions and len(self.list_2) <= 16:
                    self.list_2.append(package)
                    self.loaded_packages.append(package)

    # Check to see if packages have a specific time deadline, or if they need to be delivered by 'EOD"
    # If they have a time deadline, load them onto the first truck until full / O(n)
    def package_deadline(self, package_list):
        for package in package_list:
            if package in self.loaded_packages:
                continue
            else:
                if package.deadline is not None:
                    if package not in self.list_1 and len(self.list_1) < self.max_amount:
                        self.list_1.append(package)
                        self.loaded_packages.append(package)
                    elif len(self.list_2) < 16:
                        self.list_2.append(package)
                        self.loaded_packages.append(package)
                    else:
                        self.list_3.append(package)
                        self.loaded_packages.append(package)

    # Finish loading the rest of the packages between the trucks: / O(n)
    def greed_load(self, package_list):
        for package in package_list:
            if package in self.loaded_packages:
                continue
            else:
                if len(self.list_1) < self.max_amount:
                    self.list_1.append(package)
                    self.loaded_packages.append(package)
                elif len(self.list_1) and len(self.list_2) < self.max_amount:
                    self.list_2.append(package)
                    self.loaded_packages.append(package)
                else:
                    self.list_3.append(package)
                    self.loaded_packages.append(package)

    # Create a final sort to complete everything post "pre-sort"
