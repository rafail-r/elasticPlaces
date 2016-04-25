# coding: utf-8

from elasticsearch import Elasticsearch

# Establish Connection with Elasticsearch
es = Elasticsearch()


name_query = {
  	"query": {
    	"match" : {
    		"name" : raw_input("Search for place name = ")
    	}
  	}
}

res = es.search(index="elasticplaces", body=name_query)

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
	print hit['_source']['name']
print("\n")

near_me_query = {
  	"query": {
    	"filtered": {
      		"filter": {
        		"geo_distance": {
          			"distance": raw_input("Search in radius = ") + "m", 
          			"location": { 
            			"lat":  37.976277,
            			"lon":  23.721380
          			}
        		}
      		}
    	}
  	}
}

res = es.search(index="elasticplaces", body=near_me_query)

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
	print hit['_source']['name']
print("\n")

named_near_me_query = {
  	"query": {
  		"bool": {
  			"must": [
  				{ "match" : { "name" : raw_input("Search for place name = ") }},
    			{ "filtered": {
      				"filter": {
        				"geo_distance": {
          					"distance": raw_input("and in radius = ") + "m", 
          					"location": { 
            					"lat":  37.976277,
            					"lon":  23.721380
          					}
        				}
      				}
    			}}
    		]
  		}	
  	}
}

res = es.search(index="elasticplaces", body=named_near_me_query)

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
	print hit['_source']['name'] + ", with score = " + str(hit['_score'])
print("\n")