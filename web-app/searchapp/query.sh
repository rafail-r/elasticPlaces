curl -XPOST 'localhost:9200/elasticplaces/places/_search?pretty' -d '
{
  "size" : 5,
   "query":{
      "function_score":{
         "query":{
            "bool":{
               "should":[
                  {
                     "match":{
                        "name":{
                           "query":"bar",
                           "boost":5
                        }
                     }
                  },
                  {
                     "match":{
                        "formatted_address":{
                           "query":"bar",
                           "boost":1
                        }
                     }
                  },
                  {
                     "match":{
                        "types":{
                           "query":"bar",
                           "boost":3
                        }
                     }
                  }
               ],
               "filter" : {
                  "geo_distance" : {
                      "distance" : "10km",
                      "location" : {
                          "lat" : 38.0444634,
                          "lon" : 23.7775898
                      }
                  }
              }
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
'