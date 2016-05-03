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

def rest_name(request):
    search_key = request.GET['search']
    results = es_query(search_key, 3)
    return JsonResponse({'res' : results})

def rest_id(request):
    search_id = request.GET['id']
    res = elastic_client.get(index="elasticplaces", doc_type='places', id= search_id)
    result = res['_source']
    result['id'] = res['_id']
    return JsonResponse({'res' : result})

def rest_near(request):
    search_key = request.GET['search']
    search_radius = request.GET['radius']
    search_lat = request.GET['lat']
    search_lon = request.GET['lon']
    
    results = es_query(search_key, 3)
    return JsonResponse({'res' : results})

# query elasticsearch with keyword, display at results.html
def search_results(request):
    search_key = request.GET['search']
    results = es_query(search_key, max_size)
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
    if request.method == "POST":
        search_key = request.POST['search_text']
        results = es_query(search_key, 5)
    return render(request, 'searchapp/ajax_search.html', {'results' : results})

def es_query(search_key, results_size):
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
    res = elastic_client.search(index=index_name, body=search_query, size=results_size)
    for item in res['hits']['hits']:
        temp = {}
        temp['name'] = item['_source']['name']
        temp['formatted_address'] = item['_source']['formatted_address']
        temp['id'] = item['_id']
        results.append(temp)
    return results