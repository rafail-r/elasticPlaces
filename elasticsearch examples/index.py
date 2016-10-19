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
	            			"a => α", "A => Α",
	            			"b => β", "B => Β", 
	            			"d => δ", "D => Δ",
	            			"e => ε", "E => Ε",
	            			"f => φ", "F => Φ",
	            			"g => γ", "G => Γ",
	            			"h => η", "H => Η",
	            			"i => ι", "I => Ι",
	            			"k => κ", "K => Κ",
	            			"l => λ", "L => Λ",
	            			"m => μ", "M => Μ",
	            			"n => ν", "N => Ν",
	            			"o => ο", "O => Ο",
	            			"p => π", "P => Π",
	            			"r => ρ", "R => Ρ",
	            			"s => σ", "S => Σ",
	            			"t => τ", "T => Τ",
	            			"u => υ", "U => Υ",
	            			"v => β", "V => Β",
	            			"w => ω", "W => Ω",
	            			"x => χ", "X => Χ",
	            			"y => υ", "Y => Υ",
	            			"z => ζ", "Z => Ζ",
	            			"ks => ξ",
	            			"ps => ψ",
	            			"th => θ"
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
	        		}
	      		}
	    	}
	  	},
	  	"mappings": {
	    	"places": {
	      		"properties": {
	        		"name": {
	          			"type": "string",
	          			"analyzer": "my_analyzer"
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
