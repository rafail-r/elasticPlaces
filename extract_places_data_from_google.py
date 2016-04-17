# coding: utf-8
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
mongo_client = MongoClient()['elasticPlaces']['places']

debug_flag = 1
api_key = "AIzaSyDeXdp2tLi0n7GjZOYalJmgXwOZ9N_pBuE"
radius = 50 
coord_step = 750 # ~75m
square_side = 20  # 20 x ~75m = ~1.500m each side of the square
start_x = 0
start_y = 18 # last request stoped at (start_x, start_y) so we are continuing the requests from there

def debug(*printables):
	if debug_flag:
		if len(printables) == 0:
			print()
		for a in printables:
			print(a)

def search_square(x, y, steps):		
	for i in range(start_x, steps):
		if (i!=start_x):
			start_y = 0
		for j in range(start_y, steps):
			y += coord_step
			debug("(i, j) = (%d, %d)" %(i, j))
			nearbysearch(x, y)
		x += coord_step
		
def nearbysearch(x, y):
	location = str(x)[:2] + "." + str(x)[2:] + "," + str(y)[:2] + "." + str(y)[2:]
	token_parameter = ""
	payload = {'location': location, 'key': api_key, 'radius': radius}
	nearby_search_link = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

	nearby_response = requests.get(nearby_search_link, params=payload)
	debug(nearby_response.url)
	nearby_response_json = nearby_response.json()

	parse_page(nearby_response_json)
	while "next_page_token" in nearby_response_json:
		debug()
		debug("new page")
		debug()
		token = nearby_response_json["next_page_token"]
		payload["pagetoken"] = token
		nearby_response = requests.get(nearby_search_link, params=payload)
		nearby_response_json = nearby_response.json()
		debug(nearby_response.url)
		parse_page(nearby_response_json)

def parse_page(res):
	for result in res["results"]:
		place_id = result["place_id"]
		place_details_link = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + \
							  place_id + "&key=" + api_key
		re = requests.get(place_details_link)
		debug(re.url)
		det = re.json()["result"]
		to_be_deleted = ["place_id", \
						 "vicinity", \
						 "utc_offset", \
						 "reference", \
						 "id", \
						 "adr_address", \
						 "address_components", \
						 "scope", \
						 "alt_ids", \
						 "permanently_closed", \
						 "photos", \
						 "international_phone_number"]
		try:
			del det["opening_hours"]["open_now"]
		except KeyError:
			pass
		try:
			del det["geometry"]["access_points"]
		except KeyError:
			pass
		try:
			del det["geometry"]["viewport"]
		except KeyError:
			pass	
		for elem in to_be_deleted:
			try:
				del det[elem]
			except KeyError:
				pass
		det["_id"] = place_id
		try:
			mongo_client.insert(det)
		except DuplicateKeyError:
			pass		
		debug(det["name"])

x = 37976277
y = 23721380
debug()
debug()
#search_square(x, y, square_side)
