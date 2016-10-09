from queries import searchQuery, nearSearchQuery, autocompleteQuery
from apps import mongo_client, elastic_client, index_name, max_size

def find_nearme(search_key, lat, lon, results_size):
    search_query = nearSearchQuery(search_key, lat, lon)
    return parse_results(search_query, results_size)
    
def find(search_key, results_size):
    search_query = searchQuery(search_key)
    return parse_results(search_query, results_size)

def autocomplete(search_key, results_size):
    search_query = autocompleteQuery(search_key)
    return parse_results(search_query, results_size)

def parse_results(search_query, results_size):
    separator = ','
    results = []
    res = elastic_client.search(index=index_name, body=search_query, size=results_size)
    for item in res['hits']['hits']:    
        temp = {}
        temp['name'] = item['_source']['name']
        temp['formatted_address'] = item['_source']['formatted_address'].split(separator, 1)[0]
        temp['id'] = item['_id']
        temp['types'] = item['_source']['types']
        try:
            temp['rating'] = item['_source']['rating']
        except KeyError:
            temp['rating'] = "-"
        results.append(temp)
    return results