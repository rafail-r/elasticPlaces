# coding: utf-8

import pymongo, pyelasticsearch, elasticsearch
from pymongo import MongoClient
from bson.objectid import ObjectId
from elasticsearch import helpers


# Establish Connection with Elasticsearch
elastic_client_official   = elasticsearch.Elasticsearch(['http://83.212.96.164:9200'])
elastic_client_unofficial = pyelasticsearch.client.ElasticSearch(['http://83.212.96.164:9200'])


# Establish Connection with MongoDB
mongo_client = MongoClient()['elasticPlaces']['places']

bulk_size = 1000

# using the official elasticsearch api for python
def sync_official():
	array = []
	packet = 0
	for place in mongo_client.find({}, {"name": 1, "types": 1, "formatted_address": 1, "rating": 1, "geometry.location": 1}):
		if ((place["types"][0] == "route") or (place["types"][0] == "street_address")):
			continue
		place["_id"] = str(place["_id"])
		place["_index"] = "elasticplaces"
		place["_type"] = "places"
		array.append(place)
		packet += 1
	
		if (packet == bulk_size):
			helpers.bulk(elastic_client_official, array)
			packet = 0
			array = []

	if (array):
		helpers.bulk(elastic_client_official, array)

# using the pyelasticsearch unofficial api
def sync_unofficial():
	array = []
	packet = 0
	for place in mongo_client.find({}, {"name": 1, "types": 1, "formatted_address": 1, "rating": 1, "geometry.location": 1}):
		place["_id"] = str(place["_id"])
		array.append(place)
		packet += 1
	
		if (packet == bulk_size):
			elastic_client_unofficial.bulk_index("elasticplaces", "places", array, id_field="_id")
			packet = 0
			array = []

	if (array):
		elastic_client_unofficial.bulk_index("elasticplaces", "places", array, id_field="_id")

sync_official()
