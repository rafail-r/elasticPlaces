# coding: utf-8
from __future__ import division
import random, string, pymongo, sys

collection = pymongo.MongoClient()['elasticPlaces']['places']
size = int(sys.argv[1])
bulk_size = 1000

def main():
	arr = []
	cstart = collection.count()
	packet = 0
	for i in range(size):
		place = {
		    "name" : "" ,
		    "geometry" : {
			"location" : {
			    "lat" : 0.0,
			    "lng" : 0.0
			}
		    },
		    "url" : "",
		    "formatted_address" : "",
		    "types" : ["bar", "route"],
		    "icon" : ""
		}
		place['name'] = randomword(50)
		place['geometry']['location']['lat'] = random.randint(379500009, 379999999)/10000000
		place['geometry']['location']['lng'] = random.randint(237200000, 239999999)/10000000
		place['url'] = randomword(100)
		place['formatted_address'] = randomword(50)
		place['icon'] = randomword(50)
		arr.append(place)
		packet += 1
		if (packet == bulk_size or i == (size - 1)):
			collection.insert_many(arr, False)
			packet = 0
			arr = []
	
	cstop = collection.count()
	print(cstop - cstart)


def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

main()
