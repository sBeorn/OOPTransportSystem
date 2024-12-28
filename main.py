from abc import ABC, abstractmethod

class Database:
    def __init__(self):
        self.data = []

class Manager(ABC):
    def __init__(self, db):
        self.db = db

    @abstractmethod
    def list_items(self):
        pass

    @abstractmethod
    def add_item(self, *args):
        pass

    @abstractmethod
    def remove_item(self, identifier):
        pass

class BusManager(Manager):
    def list_items(self):
        if not self.db.data:
            print("\033[31mNo buses have been added yet!\033[m")
        else:
            print("\n\033[34m--- BUS INFORMATION ---\033[m")
            print(f"{'Bus Model':<20} | {'License Plate':<15} | {'Kilometers'}")
            print("-" * 50)
            for index, bus in enumerate(self.db.data, start=1):
                print(f"{index:<3} {bus}")
            print("-" * 50)

    def add_item(self, model, license, km):
        self.db.data.append(f"{model:<20} | {license:<15} | {km} KM")
        print("\033[32mBus added successfully!\033[m")

    def remove_item(self, license):
        for item in self.db.data:
            if license in item:
                self.db.data.remove(item)
                print("\033[32mBus removed successfully!\033[m")
                return
        print("\033[31mA bus with this license plate was not found! Please try again.\033[m")

class DriverManager(Manager):
    
    def list_items(self):
        if not self.db.data:
            print("\033[31mNo drivers have been added yet!\033[m")
        else:
            print("\n\033[34m--- DRIVER INFORMATION ---\033[m")
            print(f"{'Name':<20} | {'Age':<5} | {'Experience'}")
            print("-" * 50)
            for index, driver in enumerate(self.db.data, start=1):
                print(f"{index:<3} {driver}")
            print("-" * 50)

    def add_item(self, name, age, experience):
        self.db.data.append(f"{name:<20} | {age:<5} | {experience} Years")
        print("\033[32mDriver added successfully!\033[m")

    def remove_item(self, name):
        for item in self.db.data:
            if name in item:
                self.db.data.remove(item)
                print("\033[32mDriver removed successfully!\033[m")
                return
        print("\033[31mA driver with this name was not found! Please try again.\033[m")

class LineManager(Manager):
    def list_items(self):
        if not self.db.data:
            print("\033[31mNo lines have been added yet!\033[m")
        else:
            print("\n\033[34m--- LINE INFORMATION ---\033[m")
            print(f"{'Line Name':<15} | {'Line Route':<20} | {'Line Time'}")
            print("-" * 50)
            for index, line in enumerate(self.db.data, start=1):
                print(f"{index:<3} {line}")
            print("-" * 50)

    def add_item(self, linename, lineroute, linetime):
        self.db.data.append(f"{linename:<15} | {lineroute:<20} | {linetime} DK")
        print("\033[32mLine added successfully!\033[m")

    def remove_item(self, linename):
        for item in self.db.data:
            if linename in item:
                self.db.data.remove(item)
                print("\033[32mLine removed successfully!\033[m")
                return
        print("\033[31mA line with this name was not found! Please try again.\033[m")

class TransportAssignment:
    def __init__(self):
        self.assignments = {}

    @staticmethod
    def is_valid_assignment(bus, driver, line):
        return bus and driver and line

    def assign_bus_driver_line(self, bus, driver, line):
        if self.is_valid_assignment(bus, driver, line):
            if line not in self.assignments:
                self.assignments[line] = []
            self.assignments[line].append({"bus": bus, "driver": driver})
            print(f"\033[32mBus '{bus}' is assigned to Driver '{driver}' on Line '{line}'.\033[m")
        else:
            print("\033[31mInvalid assignment! Please ensure bus, driver, and line are selected.\033[m")

    def remove_assignment(self, bus, driver, line):
        if line in self.assignments:
            self.assignments[line] = [assignment for assignment in self.assignments[line]
                                       if assignment["bus"] != bus or assignment["driver"] != driver]
            print(f"\033[32mAssignment for Bus '{bus}' and Driver '{driver}' removed from Line '{line}'.\033[m")
        else:
            print("\033[31mAssignment not found.\033[m")

    def list_assignments(self):
        if not self.assignments:
            print("\033[31mNo assignments found!\033[m")
        else:
            print("\n\033[34m--- ASSIGNMENTS ---\033[m")
            for line, buses in self.assignments.items():
                print(f"Line: {line}")
                for assignment in buses:
                    print(f"    Bus: {assignment['bus']} - Driver: {assignment['driver']}")
            print("-" * 50)

class PublicTransportSystem:
    def __init__(self):
        self.buses_db = Database()
        self.drivers_db = Database()
        self.lines_db = Database()
        self.bus_manager = BusManager(self.buses_db)
        self.driver_manager = DriverManager(self.drivers_db)
        self.line_manager = LineManager(self.lines_db)
        self.assignment_manager = TransportAssignment()

    def menu(self):
        while True:
            print('''\033[33m
             ))))
            ((((  
          +-----+
          |     |] - WELCOME TO THE PUBLIC TRANSPORTATION SYSTEM -
          `-----' 

          ------ SYSTEM MENU ------ 
          1- Line Manager
          2- Bus Manager
          3- Driver Manager
          4- Assignment Manager
          -------------------------

          Type "off" to log out from the system.\033[m
            ''')

            user_choice = input("Select the menu you want to enter (1/2/3/4 or 'off'): ").strip().lower()
            if user_choice == "off":
                print("\033[31m<<GOODBYE!>>\033[m")
                break
            elif user_choice == "1":
                self.line_menu()
            elif user_choice == "2":
                self.bus_menu()
            elif user_choice == "3":
                self.driver_menu()
            elif user_choice == "4":
                self.assignment_menu()
            else:
                print("\033[31mError. Please choose an available option.\033[m")

    def line_menu(self):
        while True:
            print("\n\033[34m--- LINE MANAGER ---\033[m")
            print("1- View Lines")
            print("2- Add New Line")
            print("3- Delete Line Information")
            print("4- Back to Main Menu")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.line_manager.list_items()
            elif choice == "2":
                linename = input("Enter the line name: ").strip()
                lineroute = input("Enter the line route: ").strip()
                linetime = input("Enter the line time (in minutes): ").strip()
                try:
                    linetime = int(linetime)
                    self.line_manager.add_item(linename, lineroute, linetime)
                except ValueError:
                    print("\033[31mInvalid time! Please enter a number.\033[m")
            elif choice == "3":
                linename = input("Enter the line name to delete: ").strip()
                self.line_manager.remove_item(linename)
            elif choice == "4":
                print("\033[33mReturning to the main menu...\033[m")
                break
            else:
                print("\033[31mError: Invalid option.\033[m")

    def bus_menu(self):
        while True:
            print("\n\033[35m--- BUS MANAGER ---\033[m")
            print("1- View Buses")
            print("2- Add New Bus")
            print("3- Delete Bus Information")
            print("4- Back to Main Menu")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.bus_manager.list_items()
            elif choice == "2":
                model = input("Enter the bus model: ").strip()
                license = input("Enter the license plate: ").strip()
                km = input("Enter the kilometers: ").strip()
                try:
                    km = int(km)
                    self.bus_manager.add_item(model, license, km)
                except ValueError:
                    print("\033[31mInvalid kilometers! Please enter a number.\033[m")
            elif choice == "3":
                license = input("Enter the license plate to delete: ").strip()
                self.bus_manager.remove_item(license)
            elif choice == "4":
                print("\033[33mReturning to the main menu...\033[m")
                break
            else:
                print("\033[31mError: Invalid option.\033[m")

    def driver_menu(self):
        while True:
            print("\n\033[36m--- DRIVER MANAGER ---\033[m")
            print("1- View Drivers")
            print("2- Add New Driver")
            print("3- Delete Driver Information")
            print("4- Back to Main Menu")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.driver_manager.list_items()
            elif choice == "2":
                name = input("Enter the driver's name: ").strip()
                age = input("Enter the driver's age: ").strip()
                experience = input("Enter the driver's experience in years: ").strip()
                try:
                    age = int(age)
                    experience = int(experience)
                    self.driver_manager.add_item(name, age, experience)
                except ValueError:
                    print("\033[31mInvalid input! Age and experience should be numbers.\033[m")
            elif choice == "3":
                name = input("Enter the driver's name to delete: ").strip()
                self.driver_manager.remove_item(name)
            elif choice == "4":
                print("\033[33mReturning to the main menu...\033[m")
                break
            else:
                print("\033[31mError: Invalid option.\033[m")

    def assignment_menu(self):
        while True:
            print("\n\033[37m--- ASSIGNMENT MANAGER ---\033[m")
            print("1- Assign Bus to Driver on Line")
            print("2- Remove Bus-Driver-Line Assignment")
            print("3- List Assignments")
            print("4- Back to Main Menu")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                bus = input("Enter the bus model: ").strip()
                driver = input("Enter the driver's name: ").strip()
                line = input("Enter the line name: ").strip()
                self.assignment_manager.assign_bus_driver_line(bus, driver, line)
            elif choice == "2":
                bus = input("Enter the bus model to remove: ").strip()
                driver = input("Enter the driver's name to remove: ").strip()
                line = input("Enter the line name to remove: ").strip()
                self.assignment_manager.remove_assignment(bus, driver, line)
            elif choice == "3":
                self.assignment_manager.list_assignments()
            elif choice == "4":
                print("\033[33mReturning to the main menu...\033[m")
                break
            else:
                print("\033[31mError: Invalid option.\033[m")

if __name__ == "__main__":
    system = PublicTransportSystem()
    system.menu()
