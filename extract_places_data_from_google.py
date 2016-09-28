# coding: utf-8
from __future__ import print_function
import sys, requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
keys = ["AIzaSyDeXdp2tLi0n7GjZOYalJmgXwOZ9N_pBuE", "AIzaSyA619DlJdmKSc3AhXmDzNQ5C6uADYDNLIY", "AIzaSyCnnQU816-EFFF3TZb40VVwK5amgHDe898", "AIzaSyDkEJt-VbEiVbP65dyA9zto4gK_iZ2UJ98", "AIzaSyAgOvp9yaawBBNwmDmYhhDdUV_J40VjGRA", "AIzaSyC0MMXKTOYO6K4fx4MNhlNB_gagGv6gvQ4", "AIzaSyCszW6DQvXrxHwDpOBp0kdugBdo_zT0be0", "AIzaSyANMqU2q5r6vnf0ta8QPiuXtW6f0hMNXFg", "AIzaSyC6g_rYR3eMWZL4Jf8WjOUW4xldp5eT0Ys", "AIzaSyChdFiV1z6b0B3NLNRLx-Ve37Hk-he8A8k", "AIzaSyANRYW7M83NVezGgNr-st9u0VihQ1ghI7s", "AIzaSyDoIEdsnjbar6YWTuOtqKkNT0bgpVmV6NY", "AIzaSyAB555DIAufHdlPnCeKmykUj9Mkw75U68o"]

mongo_client = MongoClient()['elasticPlaces']['places']

debug_flag = True
key_index = 0
api_key = keys[key_index]
radius = 50 
coord_step = 750 # ~75m
square_side = 200  # 20 x ~75m = ~1.500m each side of the square

#ta cont einai pou stamatise xtes, kai pou sinexizei simera
i_cont = 27
j_cont = 66
x = 37948124
y = 23623072

#ta stop einai gia tipoma pou vriskete
i_stop = 0
j_stop = 0

fields_to_be_deleted = ["place_id", \
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
						"international_phone_number"
						]

def debug(*printables):
	if debug_flag:
		if len(printables) == 0:
			print()
		for a in printables:
			print(a)

# gets data for all places (or at least most of them) in a square defined by the 
# (x, y) coordinates 
def search_square():
	global i_stop, j_stop
	real_x = x + i_cont * coord_step
	real_y = y + j_cont * coord_step
	for j in range(j_cont, square_side):
		debug("(i, j) = (%d, %d)" %(i_cont, j))
		#debug("(real_xreal_x, real_y) = (%d, %d)" %(real_x, real_y))
		i_stop = i_cont
		j_stop = j
		nearbysearch(real_x, real_y)
		real_y += coord_step

	real_x += coord_step
	real_y = y
	for i in range(i_cont + 1, square_side):
		for j in range(square_side):
			debug("(i, j) = (%d, %d)" %(i, j))
			i_stop = i
			j_stop = j
			#debug("(real_xreal_x, real_y) = (%d, %d)" %(real_x, real_y))
			nearbysearch(real_x, real_y)
			real_y += coord_step
		real_y = y
		real_x += coord_step
		
# submits a request for places around the (x, y) coordinates, and stores the data
def nearbysearch(x, y):
	global api_key, key_index
	location = str(x)[:2] + "." + str(x)[2:] + "," + str(y)[:2] + "." + str(y)[2:]
	token_parameter = ""
	payload = {'location': location, 'key': api_key, 'radius': radius}
	nearby_search_link = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

	nearby_response = requests.get(nearby_search_link, params=payload)
	debug(nearby_response.url)
	nearby_response_json = nearby_response.json()
	if (nearby_response_json['status'] == "OVER_QUERY_LIMIT"):
		key_index = key_index+1
		debug("will be using key %d" %key_index)
		try:
			api_key = keys[key_index]
		except IndexError:
			debug("(i, j) = (%d, %d)" %(i_stop, j_stop))
			sys.exit()
		debug("now using key %d" %key_index)
	parse_page(nearby_response_json)

	# handle the next pages if any exist
	while "next_page_token" in nearby_response_json:
		#debug()
		debug("new page")
		#debug()
		token = nearby_response_json["next_page_token"]
		payload["pagetoken"] = token
		nearby_response = requests.get(nearby_search_link, params=payload)
		debug(nearby_response.url)
		nearby_response_json = nearby_response.json()
		parse_page(nearby_response_json)

# parses the response page, requests details for each place in it and stores the 
# relevant data in our database
def parse_page(page):
	global api_key, key_index
	for place in page["results"]:
		place_id = place["place_id"]
		place_details_link = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + \
							  place_id + "&key=" + api_key
		place_details_response = requests.get(place_details_link)
		debug(place_details_response.url)
		try:
			place_details_json = place_details_response.json()["result"]
		except KeyError:
			key_index = key_index+1
			debug("will try using key %d" %key_index)
			try:
				api_key = keys[key_index]
			except IndexError:
				debug("(i, j) = (%d, %d)" %(i_stop, j_stop))
				sys.exit()
			debug("now using key %d" %key_index)
			continue

		# delete the fields (if they exist) that we are not interested in
		for elem in fields_to_be_deleted:
			try:
				del place_details_json[elem]
			except KeyError:
				# if you try to delete a field that is not there ignore it
				pass
		# also delete some nested fields we are not interested in
		try:
			del place_details_json["opening_hours"]["open_now"]
		except KeyError:
			pass
		try:
			del place_details_json["geometry"]["access_points"]
		except KeyError:
			pass
		try:
			del place_details_json["geometry"]["viewport"]
		except KeyError:
			pass	

		# use the place_id field as the mongodb special _id field and insert the json in the db
		place_details_json["_id"] = place_id
		try:
			mongo_client.insert(place_details_json)
		except DuplicateKeyError:
			# when the place is already in the db just ignore it
			pass		
		debug(place_details_json["name"])




debug()
debug()
search_square()
