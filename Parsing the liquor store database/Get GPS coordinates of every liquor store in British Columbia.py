# Created by Bennett
# This is public domain. Everyone should be able to find their nearest liquor store XD

# Geopy's docs: https://geopy.readthedocs.io/en/stable/#googlev3
# Google's Github for the maps python API: https://geopy.readthedocs.io/en/stable/#googlev3

from geopy.geocoders import Nominatim
import googlemaps
import csv
import time
import re
import json

LiquorStoreAddresses = []

with open('Parsing the liquor store database/Every liquor store in bc.csv', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        LiquorStoreAddresses.append(row)

# Uses the Nominatim software from OpenStreetMaps. It's free but it has a limit of 1 API call/second
# and it requires pretty specific adress formating
# I was able to parse roughly 2/3 of the addresses using this
def freeGeocodeParser():
    # Create a geolocator object with a user agent
    geolocator = Nominatim(user_agent="Getting Liquor Store Coordinates")
    
    counter = 0
    for item in LiquorStoreAddresses:
        if len(item) <= 4:
            # Define the address to geocode
            address = str(item[1]) + ", " + str(item[2]) + ", British Columbia" #, Canada, " + str(item[4])

            # Geocode the address
            location = geolocator.geocode(address, timeout= 10)

            # Extract and print the coordinates
            if location:
                item.append(location.latitude)
                item.append(location.longitude)
                print(str(counter) + f" {item}")
            else:
                print(str(counter) + f" Could not find coordinates for: {address}")
                item.append("failed")
                item.append("failed")

            #sleep because Nominatim has a crap API limit
            time.sleep(1)
            counter +=1
            if counter >= 800:
                break
        else:
            print(item)

    with open('Parsing the liquor store database/Every liquor store in bc.csv', 'w', newline='') as file:
        writer =csv.writer(file)
        writer.writerows(LiquorStoreAddresses)

# Uses the google maps API to parse addresses and get coordinates. It's a lot better at interpretting
# poorly formatted addresses, but it costs money. You get 10,000 free API calls, after which it charges
# $5 per 1000 API calls, so this should only be used for the bad addresses
def moneyGeocodeParser():
    counter = 0

    APIkey = ''
    # Making a file to cache the returned info in case I want to use anything else later without making more API calls
    AddressDatabase = []
    
    #Get API key from file on local machine so I don't expose in on Github like a dumbass
    with open('Google_Maps_API_Key.txt','r') as file:
        APIkey = file.read()

    gmaps = googlemaps.Client(key=APIkey)

    for item in LiquorStoreAddresses:
        if len(item) <= 4:
            #build address for querry
            address = f"{item[1]}, {item[2]}, British Columbia, Canada"

            try:
                #geocode address using google maps api (costs actual money)
                result = gmaps.geocode(address)

                if result:
                    lat = result[0]['geometry']['location']['lat']
                    lng = result[0]['geometry']['location']['lng']
                    item.append(lat)
                    item.append(lng)
                    print(f"{counter} {item}")
                    AddressDatabase.append(result[0])
                else:
                    print(f"{counter} Could not find coordinates for: {address}")
                    item.append("failed")
                    item.append("failed")
            except Exception as e:
                print(f"{counter} Error geocoding {address}: {e}")
                item.append("error")
                item.append("error")

            time.sleep(0.1)  # Google API rate limits are higher
            counter += 1

            if counter >= 1200:
                break
        else:
            print(item)

    with open('Parsing the liquor store database/Every liquor store in bc.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(LiquorStoreAddresses)

    with open("address.json","w") as file:
        json.dump(AddressDatabase, file, indent=4)

# make array for the arduino
def makeArrayforArduino():
    array = []
    with open("Reformatted Liquor Store Addresses.csv",'r') as file:
        reader =csv.reader(file)
        for row in reader:
            array.append(row)
    for row in array:
        row[1] = str(row[1])
        row[1] = row[1][:2]+row[1][3:6]
        row[2] = str(row[2])
        row[2] = row[2][2:4]+row[2][5:8]
    
    with open("coordinatesArray.txt",'w') as file:
        for i in range(1,len(array)):
            file.write("{"+array[i][1]+','+array[i][2]+"},\n")

# function to rewrite the CSV from the Google Maps JSON file because they seem to be wrong
def rewriteGPScoords(filename):
    addresses = []
    with open(filename, 'r') as file:
        addresses = json.load(file)

    addressArray = []    

    for item in addresses:
       address = []
       address.append(item["formatted_address"])
       address.append(item["geometry"]["location"]["lat"])
       address.append(item["geometry"]["location"]["lng"])
       addressArray.append(address)

    with open("Reformatted Liquor Store Addresses.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Address','lat','lng']
        writer.writerow(header)
        writer.writerows(addressArray)




# Comment out whichever geocoder you don't want to use

# freeGeocodeParser()
# moneyGeocodeParser()
# rewriteGPScoords('address.json')
makeArrayforArduino()

