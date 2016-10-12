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
                                   "boost":2
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
                          "missing":2
                       }
                    }
                 ],
                 "boost_mode": "avg"
              }
           }
        }

#def autocompleteQuery(search_key):
#  return  {
#    "query":{
#      "multi_match" : {
#        "query":search_key,
#        "type":"phrase_prefix",
#        "max_expansions" : 1000,
#        "fields":[ "name^5", "formatted_address^2", "types^3"]
#      }
#    }
#  }

def autocompleteQuery(search_key):
  return  {
    "query":{
      "multi_match" : {
        "query":search_key,
        "type":"phrase_prefix",
        "max_expansions" : 1000,
        "fields":[ "name"]
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