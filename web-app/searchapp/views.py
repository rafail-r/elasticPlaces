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

# query mongodb with keyword, display at results.html
def search_results(request):
    search_key = request.GET['search']
    title_results = mongo_client.find({'title': {'$regex' : '.*' + search_key + '.*'}})
    results = []
    for i in title_results:
        temp = {
            "id"    : i['_id'],
            "title" : i['title']
        }
        results.append(temp)
    return render(request, "searchapp/results.html", {'res' : results})

# query mongodb with id, display at details.html
def get_by_id(request, _id):
    print _id
    title_results = mongo_client.find({'_id': _id})
    results = []
    for i in title_results:
        temp = {
            "id"    : i['_id'],
            "title" : i['title']
        }
        results.append(temp)
    return render(request, "searchapp/details.html", {'res' : results})

# ajax-livesearch
def live_search(request):
    title_results = []
    if request.method == "POST":
        search_text = request.POST['search_text']
        search_query = {
            "query" : {
                "match" : {
                    "title" : search_text
                }
            }
        }
        res = elastic_client.search(index=index_name, body=search_query)
        for item in res['hits']['hits']:
            temp = {
                "id" : item['_id'],
                "title" : item['_source']['title']
            }
            title_results.append(temp)
    return render(request, 'searchapp/ajax_search.html', {'results' : title_results})