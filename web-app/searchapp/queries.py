curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
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
         ]
      }
   }
}
'