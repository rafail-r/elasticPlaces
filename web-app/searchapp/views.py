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
    results = es_query(search_key, 20)
    return JsonResponse({'res' : results})



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
        result['website'] = res['website']
    except KeyError:
        result['website'] = " "
    try:
        result['formatted_phone_number'] = res['formatted_phone_number']
    except KeyError:
        result['formatted_phone_number'] = " "
    
    return JsonResponse({'res' : result})

def rest_near(request):
    search_key = request.GET['search']
    #search_radius = request.GET['radius']
    search_lat = request.GET['lat']
    search_lon = request.GET['lon']
    results = es_nearme(search_key, search_lat, search_lon, 20)
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

# query mongodb with id, display at details.html
def get_by_id(request, _id):
    result = mongo_client.find_one({"_id": _id})
    result['id'] = result['_id']

    return render(request, "searchapp/details.html", {'res' : result})

# ajax-livesearch
def live_search(request):
    if request.method == "POST":
        search_key = request.POST['search_text']
        results = es_query(search_key, 5)
    return render(request, 'searchapp/ajax_search.html', {'results' : results})

def es_nearme(search_key, lat, lon, results_size):
    separator = ','
    search_query = nearSearchQuery(search_key, lat, lon)
    results = []
    res = elastic_client.search(index=index_name, body=search_query, size=results_size)
    for item in res['hits']['hits']:    
	temp = {}
        temp['name'] = item['_source']['name']
        temp['formatted_address'] = item['_source']['formatted_address'].split(separator, 1)[0]
        temp['id'] = item['_id']
	temp['types'] = item['_source']['types'][0]
	try:
		temp['rating'] = item['_source']['rating']
	except KeyError:
		temp['rating'] = 0.
        results.append(temp)
    return results
    
def es_query(search_key, results_size):
    separator = ','
    search_query = searchQuery(search_key)
    results = []
    res = elastic_client.search(index=index_name, body=search_query, size=results_size)
    for item in res['hits']['hits']:    
	temp = {}
        temp['name'] = item['_source']['name']
        temp['formatted_address'] = item['_source']['formatted_address'].split(separator, 1)[0]
        temp['id'] = item['_id']
	temp['types'] = item['_source']['types'][0]
	try:
		temp['rating'] = item['_source']['rating']
	except KeyError:
		temp['rating'] = 0.
        results.append(temp)
    return results


def searchQuery(search_key):
    return  {
           "query":{
              "function_score":{
                 "query":{
                    "bool":{
                       "should":[
                          {
                             "match":{
                                "name":{
                                   "query":search_key,
                                   "boost":5
                                }
                             }
                          },
                          {
                             "match":{
                                "formatted_address":{
                                   "query":search_key,
                                   "boost":1
                                }
                             }
                          },
                          {
                             "match":{
                                "types":{
                                   "query":search_key,
                                   "boost":3
                                }
                             }
                          }
                       ]
                    }
                 },
                 "functions":[
                    {
                       "field_value_factor":{
                          "field":"rating",
                          "factor":1.2,
                          "modifier":"sqrt",
                          "missing":2
                       }
                    }
                 ],
                 "boost_mode": "avg"
              }
           }
        }

def nearSearchQuery(search_key, lat, lon):
    return  {
               "query":{
                  "function_score":{
                     "query":{
                        "bool":{
                           "should":[
                              {
                                 "match":{
                                    "name":{
                                       "query":search_key,
                                       "boost":5
                                    }
                                 }
                              },
                              {
                                 "match":{
                                    "formatted_address":{
                                       "query":search_key,
                                       "boost":1
                                    }
                                 }
                              },
                              {
                                 "match":{
                                    "types":{
                                       "query":search_key,
                                       "boost":3
                                    }
                                 }
                              }
                           ]
                        }
                     },
                     "functions":[
                        {
                           "field_value_factor":{
                              "field":"rating",
                              "factor":1.2,
                              "modifier":"sqrt",
                              "missing":2
                           }
                        },
                        {
                           "gauss":{
                              "location":{
                                 "origin":{
                                    "lat":lat,
                                    "lon":lon
                                 },
                                 "offset":"1km",
                                 "scale":"2km"
                              }
                           },
                           "weight":1.2
                        }
                     ],
                     "boost_mode":"avg"
                  }
               }
            }
