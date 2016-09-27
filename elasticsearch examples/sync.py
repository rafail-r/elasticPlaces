# coding: utf-8

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# Establish Connection with Elasticsearch
elastic_client = Elasticsearch()

# Establish Connection with MongoDB
mongo_client = MongoClient()['elasticPlaces']['places']

bulk_size = 1000

def sync():
	array = []
	packet = 0
	for place in mongo_client.find():
		new_place = {
			"_index": "elasticplaces",
			"_type": "places",
			"_id": str(place["_id"]),
			"_source": {}
		}

		try:
			new_place["_source"]["name"] = place["name"]
		except KeyError:
			pass
		try:
			new_place["_source"]["types"] = place["types"]
		except KeyError:
			pass
		try:
			new_place["_source"]["formatted_address"] = place["formatted_address"]
		except KeyError:
			pass
		try:
			new_place["_source"]["rating"] = place["rating"]
		except KeyError:
			pass
		try:
			new_place["_source"]["geometry"]["location"] = place["geometry"]["location"]
		except KeyError:
			pass

		array.append(new_place)
		packet += 1
	
		if (packet == bulk_size):
			helpers.bulk(elastic_client, array)
			packet = 0
			array = []

	if (array):
		helpers.bulk(elastic_client, array)

sync()

