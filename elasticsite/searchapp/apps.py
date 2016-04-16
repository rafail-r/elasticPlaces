from __future__ import unicode_literals

from django.apps import AppConfig
from pymongo import MongoClient
from elasticsearch import Elasticsearch

# Establish Connection with Elasticsearch
elastic_client = Elasticsearch()
index_name = 'my_index'

# Establish Connection with MongoDB
mongo_client = MongoClient()['test_db']['books']

class SearchappConfig(AppConfig):
    name = 'searchapp'