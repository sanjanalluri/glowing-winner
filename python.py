from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import cgi

# Linking HTML and Python together
form = cgi.FieldStorage()
searchterm =  form.getvalue('Name:')
print(searchterm)

# example data includes 1 potential rider and 4 potential pickup options
# in the following format: [name, time of pick up, address]
# address only requires the building number, street name, and city (no abbreviations)

# person who needs to be picked up
rider = ["tony", "3:30", "3601 Kohnen Way, Dublin"]

# people  who can pick up
pickup1 = ["steve", "3:30", "3150 Palermo Way Dublin"]
pickup2 = ["wanda", "3:50", "3300 Antone Way Dublin"]
pickup3 = ["natasha", "3:25", "4972 Dublin Blvd Dublin"]
pickup4 = ["thor", "4:10", "4910 Dublin Blvd Dublin"]

# the main component to acurately represent location
geolocator = Nominatim(user_agent="gaelshare")

def close_distance(passenger, driver):
    # finding full address of driver and passenger
    passenger_add = geolocator.geocode(passenger[2])
    driver_add = geolocator.geocode(driver[2])

    # using full address to find exact location via (lat, long)
    passenger_loc = (passenger_add.latitude, passenger_add.longitude)
    driver_loc = (driver_add.latitude, driver_add.longitude)

    # using geodesic to find distance between passenger and driver in miles
    distance = geodesic(passenger_loc, driver_loc).miles

    # ruling out people with more than 1 mile distance between each other
    if distance <= 1.0:
        return True
    else:
        return False

def close_time(passenger, driver):
    # manipulating time of pick up into a valid 3-digit integer
    pass_simple_time = int(''.join(passenger[1].split(":")))
    driv_simple_time = int(''.join(driver[1].split(":")))
    
    # ruling out people with more than 15 minutes preffered time difference
    if abs(pass_simple_time - driv_simple_time) <= 15:
        return True
    return False

def carpool(passenger, driver):
    # combining two key decisions to determine if the pair are suitable to carpool
    if close_time(passenger, driver) == True and close_distance(passenger, driver) == True:
        return True
    return False

# Example Runs to demonstrate proper functioning
# Can Steve pick up Tony
print("Can Steve pick up Tony?")
result = carpool(rider, pickup1)
print(result)

# Can Wanda pick up Tony
print("Can Wanda pick up Tony?")
result = carpool(rider, pickup2)
print(result)

# Can Natasha pick up Tony
print("Can Natasha pick up Tony?")
result = carpool(rider, pickup3)
print(result)

# Can Thor pick up Tony
print("Can Thor pick up Tony?")
result = carpool(rider, pickup4)
print(result)