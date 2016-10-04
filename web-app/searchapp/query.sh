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
                           "boost":1
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
                           "boost":1
                        }
                     }
                  }
               ]
            }
         },
         "functions": [
            {
              "gauss": {
                "location": { 
                  "origin": { "lat": 37.948124, "lon": 23.623072 },
                  "offset": "1km",
                  "scale":  "2km"
                }
              },
              "weight": 1.2
            },
            {
              "linear": {
                "rating": { 
                  "origin": "5", 
                  "offset": "0",
                  "scale":  "3"
                }
              } 
            }
          ],
             "boost_mode": "avg"
          }
   }

}
'