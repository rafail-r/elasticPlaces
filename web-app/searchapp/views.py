# coding: utf-8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json, requests
from bson.objectid import ObjectId
from apps import mongo_client, elastic_client, index_name


# homepage
def search_page(request):
    return render(request, "searchapp/search.html")

# query elasticsearch with keyword, display at results.html
def search_results(request):
    search_key = request.GET['search']
    search_query = {
        "query": {
            "bool": {
                "should": [
                    { "match" : { "name" : search_key }},
                    { "match" : { "formatted_address" : search_key }},
                    { "match" : { "types" : search_key }}
                ]
            }
        }
    }
    results = []
    res = elastic_client.search(index=index_name, body=search_query)
    for item in res['hits']['hits']:
        temp = {}
        temp['name'] = item['_source']['name']
        temp['formatted_address'] = item['_source']['formatted_address']
        temp['id'] = item['_id']
        results.append(temp)
    return render(request, "searchapp/results.html", {'res' : results})

# query elasticsearch with id, display at details.html
def get_by_id(request, _id):
    res = elastic_client.get(index="elasticplaces", doc_type='places', id= _id)
    result = res['_source']
    result['id'] = res['_id']
    return render(request, "searchapp/details.html", {'res' : result})

# ajax-livesearch
def live_search(request):
    live_results = []
    if request.method == "POST":
        search_text = request.POST['search_text']
        search_query = {
            "query": {
                "bool": {
                    "should": [
                        { "match" : { "name" : search_text }},
                        { "match" : { "formatted_address" : search_text }},
                        { "match" : { "types" : search_text }}
                    ]
                }
            }
        }
        res = elastic_client.search(index=index_name, body=search_query)
        for item in res['hits']['hits']:
            temp = {}
            temp['name'] = item['_source']['name']
            temp['formatted_address'] = item['_source']['formatted_address']
            temp['id'] = item['_id']
            live_results.append(temp)
    return render(request, 'searchapp/ajax_search.html', {'results' : live_results})