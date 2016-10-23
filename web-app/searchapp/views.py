# coding: utf-8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json, requests
from bson.objectid import ObjectId
from apps import mongo_client, elastic_client, index_name, max_size
from helpers import find, find_nearme, autocomplete
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# homepage for the web app
def search_page(request):
    return render(request, "searchapp/search.html")

# methods for the rest interface for mobile app
# search by keyword
def rest_name(request):
    search_key = request.GET['search']
    results = find(search_key, 20)
    return JsonResponse({'res' : results})

# search by keyword and include geodata scoring
def rest_near(request):
    search_key = request.GET['search']
    search_lat = request.GET['lat']
    search_lon = request.GET['lon']
    results = find_nearme(search_key, search_lat, search_lon, 20)
    return JsonResponse({'res' : results})

# autocomplete results for live search
def rest_autocomplete(request):
    print 'gggege'
    search_key = request.GET['search']
   
    print search_key

    results = autocomplete(search_key, 5)
    return JsonResponse({'res' : results})

# get full document from mongodb
def rest_id(request):
    separator = ','
    search_id = request.GET['id']
    res = result = mongo_client.find_one({"_id": search_id})
    result = {}
    result['id'] = res['_id']
    result['name'] = res['name']
    result['formatted_address'] = res['formatted_address'].split(separator, 1)[0]
    result['lat'] = res['geometry']['location']['lat']
    result['lon'] = res['geometry']['location']['lng']
    try:
        result['rating'] = res['rating']
    except KeyError:
        result['rating'] = 0
    try:
        result['types'] = res['types']
    except KeyError:
        result['types'] = [""]
    try:
        result['website'] = res['website']
    except KeyError:
        result['website'] = " "
    try:
        result['formatted_phone_number'] = res['formatted_phone_number']
    except KeyError:
        result['formatted_phone_number'] = " "
    
    return JsonResponse({'res' : result})

# query elasticsearch with keyword, display at results.html
def search_results(request):
    search_key = request.GET['search']
    results = find(search_key, max_size)
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

# query mongodb with id, display at details.html
def get_by_id(request, _id):
    result = mongo_client.find_one({"_id": _id})
    result['id'] = result['_id']
    return render(request, "searchapp/details.html", {'res' : result})

# ajax-livesearch
def live_search(request):
    if request.method == "POST":
        search_key = request.POST['search_text']
        results = autocomplete(search_key, 5)
    return render(request, 'searchapp/ajax_search.html', {'results' : results})
