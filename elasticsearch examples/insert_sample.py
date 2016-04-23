# coding: utf-8

from elasticsearch import Elasticsearch
es = Elasticsearch()

doc1 = {
    "website" : "http://bollywood-kitchen.blogspot.gr/",
    "name" : "test Kitchen",
    "location" : {
        "lat" : 37.9764949,
        "lon" : 23.7217914
    },
    "formatted_phone_number" : "21 1401 9197",
    "url" : "https://maps.google.com/?cid=7511755221305653825",
    "formatted_address" : "Adrianou ke Thisiou 7, Athina 105 55, Greece",
    "types" : [ 
        "restaurant", 
        "food", 
        "point_of_interest", 
        "establishment"
    ],
    "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png"
}

res = es.index(index="my_index2", doc_type='places', id="ChIJb1fnICK9oRQRQfqbJZMdP2g", body=doc1)
print(res['created'])

res = es.get(index="my_index2", doc_type='places', id="ChIJb1fnICK9oRQRQfqbJZMdP2g")
print(res['_source'])

doc2 = {
    "website" : "http://bollywood-kitchen.blogspot.gr/",
    "name" : "τεστ Kitchen",
    "location" : {
        "lat" : 37.9764949,
        "lon" : 23.7217914
    },
    "formatted_phone_number" : "21 1401 9197",
    "url" : "https://maps.google.com/?cid=7511755221305653825",
    "formatted_address" : "Adrianou ke Thisiou 7, Athina 105 55, Greece",
    "types" : [ 
        "restaurant", 
        "food", 
        "point_of_interest", 
        "establishment"
    ],
    "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png"
}

res = es.index(index="my_index2", doc_type='places', id="ChIJb1fnICK9oRQRQfqbJZMdP2G", body=doc2)
print(res['created'])

res = es.get(index="my_index2", doc_type='places', id="ChIJb1fnICK9oRQRQfqbJZMdP2G")
print(res['_source'])
