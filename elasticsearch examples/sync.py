# coding: utf-8

from pymongo import MongoClient
from elasticsearch import Elasticsearch

# Establish Connection with Elasticsearch
elastic_client = Elasticsearch()

# Establish Connection with MongoDB
mongo_client = MongoClient()['elasticPlaces']['places']

for place in mongo_client.find():
	place_id = place['_id']
	place_lat = place['geometry']['location']['lat']
	place_lon = place['geometry']['location']['lng']
	try:
		del place['_id']
	except KeyError:
		pass
	try:
		del place['geometry']
	except KeyError:
		pass
	place['location'] = {
		'lat' : place_lat,
		'lon' : place_lon
	}
	res = elastic_client.index(index='elasticplaces', doc_type='places', id=place_id, body=place)