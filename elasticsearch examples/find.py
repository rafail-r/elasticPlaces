# coding: utf-8

from elasticsearch import Elasticsearch
es = Elasticsearch()

print("\nsearching for test")
res = es.search(index="my_index2", body={"query": {"match": {
      "name" : "test"
    }}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
	title_test = hit['_source']['name']
	print title_test
print("\n")



print("searching for τεστ")
res = es.search(index="my_index2", body={"query": {"match": {
      "name" : "τεστ"
    }}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
	title_test = hit['_source']['name']
	print title_test
print("\n")

print("everything in the database:")
res = es.search(index="my_index2", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
	title_test = hit['_source']['name']
	print title_test
print("\n")
