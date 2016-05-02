# coding: utf-8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json, requests
from bson.objectid import ObjectId
from apps import mongo_client, elastic_client, index_name, max_size
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# homepage
def search_page(request):
    return render(request, "searchapp/search.html")

def rest(request):
    return JsonResponse({'message': 'Hello', 'status_code': 200})

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
    res = elastic_client.search(index=index_name, body=search_query, size=max_size)
    for item in res['hits']['hits']:
        temp = {}
        temp['name'] = item['_source']['name']
        temp['formatted_address'] = item['_source']['formatted_address']
        temp['id'] = item['_id']
        results.append(temp)
    paginator = Paginator(results, 15) # Show 15 results per page
    page = request.GET.get('page')
    try:
        page_results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_results = paginator.page(paginator.num_pages)
    return render(request, "searchapp/results.html", {'res' : page_results, 'search_key' : search_key})

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
        res = elastic_client.search(index=index_name, body=search_query, size=5)
        for item in res['hits']['hits']:
            temp = {}
            temp['name'] = item['_source']['name']
            temp['formatted_address'] = item['_source']['formatted_address']
            temp['id'] = item['_id']
            live_results.append(temp)
    return render(request, 'searchapp/ajax_search.html', {'results' : live_results})

