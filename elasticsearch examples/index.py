# coding: utf-8

from elasticsearch import Elasticsearch
es = Elasticsearch(['http://83.212.96.164:9200'])

es.indices.delete(index='elasticplaces', ignore=[400, 404])


es.indices.create(
    index="elasticplaces",
    body={
	  	"settings": {
	    	"analysis": {
	      		"char_filter": {
	        		"my_mapping": {
	         			"type": "mapping",
	          			"mappings" : [
	          				"α => a", "η => i",  "ν => n",  "υ => y",  "ΕΥ => ef", 
	          				"ά => a", "ή => i",  "Ν => n",  "Υ => y",  "αυ => af", "ου => ou",
	          				"Α => a", "Η => i",  "ξ => ks", "φ => f",  "αύ => af", "ού => ou",
	          				"Ά => a", "Ή => i",  "Ξ => ks", "Φ => f",  "Αυ => af", "Ου => ou",
	          				"β => b", "θ => th", "ο => o",  "χ => x",  "ΑΥ => af", "Ού => ou",
	          				"Β => b", "Θ => th", "ό => o",  "Χ => x",  "γκ => g",  "ΟΥ => ou",
	          				"γ => g", "ι => i",  "Ο => o",  "ψ => ps", "Γκ => g",  "ύ => y",
	          				"Γ => g", "ί => i",  "Ό => o",  "Ψ => ps", "ΓΚ => g", 
	          				"δ => d", "Ι => i",  "π => p",  "ω => o",  "γγ => g", 
	          				"Δ => d", "Ί => i",  "Π => p",  "ώ => o",  "Γγ => g", 
	          				"ε => e", "κ => k",  "ρ => r",  "Ω => o",  "ΓΓ => g", 
	          				"έ => e", "Κ => k",  "Ρ => r",  "Ώ => o",  "μπ => b", 
	          				"Ε => e", "λ => l",  "σ => s",  "ς => s",  "ευ => ef", "Μπ => b", 
	          				"Έ => e", "Λ => l",  "Σ => s",  "οι => i", "εύ => ef", "ΜΠ => b", 
	          				"ζ => z", "μ => m",  "τ => t",  "οί => i", "Ευ => ef", 
	          				"Ζ => z", "Μ => m",  "Τ => t",  "Οι => i", "Εύ => ef"
	          			]
	        		},
	        		"my_mapping_two": {
	         			"type": "mapping",
	          			"mappings" : [
	          				"α => a", "η => h",  "ν => n",  "υ => i",  "Οί => i",  "ΕΥ => ef", "ΝΤ => d",
	          				"ά => a", "ή => h",  "Ν => n",  "Υ => i",  "ΟΙ => i",  "αυ => af", "ου => ou",
	          				"Α => a", "Η => h",  "ξ => ks", "φ => f",  "αι => e",  "αύ => af", "ού => ou",
	          				"Ά => a", "Ή => h",  "Ξ => ks", "Φ => f",  "αί => e",  "Αυ => af", "Ου => ou",
	          				"β => v", "θ => th", "ο => o",  "χ => x",  "Αι => e",  "ΑΥ => af", "Ού => ou",
	          				"Β => v", "Θ => th", "ό => o",  "Χ => x",  "Αί => e",  "γκ => g",  "ΟΥ => ou",
	          				"γ => g", "ι => i",  "Ο => o",  "ψ => ps", "ΑΙ => e",  "Γκ => g",  "ύ => i",
	          				"Γ => g", "ί => i",  "Ό => o",  "Ψ => ps", "ει => i",  "ΓΚ => g", 
	          				"δ => d", "Ι => i",  "π => p",  "ω => w",  "εί => i",  "γγ => g", 
	          				"Δ => d", "Ί => i",  "Π => p",  "ώ => w",  "Ει => i",  "Γγ => g", 
	          				"ε => e", "κ => k",  "ρ => r",  "Ω => w",  "Εί => i",  "ΓΓ => g", 
	          				"έ => e", "Κ => k",  "Ρ => r",  "Ώ => w",  "ΕΙ => i",  "μπ => b", 
	          				"Ε => e", "λ => l",  "σ => s",  "ς => s",  "ευ => ef", "Μπ => b", 
	          				"Έ => e", "Λ => l",  "Σ => s",  "οι => i", "εύ => ef", "ΜΠ => b", 
	          				"ζ => z", "μ => m",  "τ => t",  "οί => i", "Ευ => ef", "ντ => d", 
	          				"Ζ => z", "Μ => m",  "Τ => t",  "Οι => i", "Εύ => ef", "Ντ => d"
	          			]
	        		}
	      		},
	      		"filter" : {
	      			"myGreekLowerCaseFilter" : {
	      				"type" : "lowercase",
	      				"language" : "greek"
	      			},
					"ngrams_filter": {
					    "type": "ngram",
					    "min_gram": 3,
					    "max_gram": 8
					}
	      		},
	      		"analyzer": {
	        		"my_analyzer": {
	          			"type": "custom", 
		  				"char_filter": ["my_mapping"],
	          			"tokenizer": "standard",
	          			"filter": ["lowercase", "myGreekLowerCaseFilter", "ngrams_filter"]
	        		},
	        		"my_analyzer_two": {
	        			"type": "custom", 
		  				"char_filter": ["my_mapping_two"],
	          			"tokenizer": "standard",
	          			"filter": ["lowercase", "myGreekLowerCaseFilter", "ngrams_filter"]
	        		}
	      		}
	    	}
	  	},
	  	"mappings": {
	    	"places": {
	      		"properties": {
	        		"name": {
	          			"type": "string",
	          			"analyzer": "my_analyzer",
	          			"fields" : {
	          				"greeklish": {
	          					"type": "string",
	          					"analyzer": "my_analyzer_two"
	          				}
	          			}
			        },
			        "formatted_address": {
	          			"type": "string",
	          			"analyzer": "my_analyzer"
	        		},
					"types": {
	          			"type": "string",
	          			"analyzer": "my_analyzer"
	        		},
	        		"location": {
          				"type": "geo_point"
	        		}
	      		}
	    	}
	  	}
	},
    # Will ignore 400 errors, remove to ensure you're prompted
    ignore=400
)
