# coding: utf-8
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
mongo_client = MongoClient()['elasticPlaces']['places']

api_key = "AIzaSyDeXdp2tLi0n7GjZOYalJmgXwOZ9N_pBuE"

def search_rect(x, y, steps):
	for i in range(steps):
		for j in range(steps):
			y += 500
			nearbysearch(x, y)
		x += 500
		
	
def nearbysearch(x, y):
	location = str(x)[:2] + "." + str(x)[2:] + "," + str(y)[:2] + "." + str(y)[2:]
	token_parameter = ""
	payload = {'location': location, 'key': api_key, 'radius': 20}
	nearby_search_link = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

	r = requests.get(nearby_search_link, params=payload)
	res = r.json()
	print(r.url)

	parse_page(res)
	while "next_page_token" in res:
		print
		print("new page")
		print
		token = res["next_page_token"]
		payload["pagetoken"] = token
		r = requests.get(nearby_search_link, params=payload)
		res = r.json()
		print(r.url)
		parse_page(res)

def parse_page(res):
	for result in res["results"]:
		place_id = result["place_id"]
		place_details_link = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=" + api_key
		re = requests.get(place_details_link)
		print(re.url)
		det = re.json()["result"]
		to_be_deleted = ["place_id", "vicinity", "utc_offset", "reference", "id", "adr_address", "address_components", "scope", "alt_ids", "permanently_closed", "photos", "international_phone_number"]
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
		print(det["name"])

x = 37976277
y = 23721380
print
print
search_rect(x, y, 2)
