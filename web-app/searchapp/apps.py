from __future__ import unicode_literals

from django.apps import AppConfig
from pymongo import MongoClient
from elasticsearch import Elasticsearch

# Establish Connection with Elasticsearch
elastic_client = Elasticsearch(['http://83.212.96.164:9200'])
index_name = 'elasticplaces'
max_size = 50

# Establish Connection with MongoDB
mongo_client = MongoClient()['elasticPlaces']['places']

class SearchappConfig(AppConfig):
    name = 'searchapp'
