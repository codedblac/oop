# Parent class: Vehicle
class Vehicle:
    def move(self):
        # A generic move method for all vehicles
        print("The vehicle is moving.")

# Child class: Car
class Car(Vehicle):
    def move(self):
        # Overriding the move method to simulate driving
        print("Driving 🚗")

# Child class: Plane
class Plane(Vehicle):
    def move(self):
        # Overriding the move method to simulate flying
        print("Flying ✈️")

# Child class: Boat
class Boat(Vehicle):
    def move(self):
        # Overriding the move method to simulate sailing
        print("Sailing ⛵")

# Function to demonstrate polymorphism
def demonstrate_move(vehicle):
    # This function accepts any object of type Vehicle (or its subclasses) and calls the move() method
    vehicle.move()

# Creating instances of different vehicles
car = Car()
plane = Plane()
boat = Boat()

# Demonstrating polymorphism
print("Demonstrating Polymorphism:")
demonstrate_move(car)   # This will call Car.move() and print "Driving 🚗"
demonstrate_move(plane)  # This will call Plane.move() and print "Flying ✈️"
demonstrate_move(boat)   # This will call Boat.move() and print "Sailing ⛵"
