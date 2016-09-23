# coding: utf-8

from elasticsearch import Elasticsearch
es = Elasticsearch()


#es.indices.refresh(index="my_index2")
es.indices.delete(index='my_index2', ignore=[400, 404])


es.indices.create(
    index="my_index2",
    body={
	  "settings": {
	    "analysis": {
	      "char_filter": {
	        "my_mapping": {
	          "type": "mapping",
	          "mappings" : [
	            "a => α",
	            "b => β", 
	            "d => δ",
	            "e => ε",
	            "f => φ",
	            "g => γ",
	            "h => η",
	            "i => ι",
	            "k => κ",
	            "l => λ",
	            "m => μ",
	            "n => ν",
	            "o => ο",
	            "p => π",
	            "r => ρ",
	            "s => σ",
	            "t => τ",
	            "u => υ",
	            "v => β",
	            "w => ω",
	            "x => χ",
	            "y => υ",
	            "z => ζ",
	            "ks => ξ",
	            "ps => ψ",
	            "th => θ"
	          ]
	        }
	      },
	      "analyzer": {
	        "my_analyzer": {
	          "type": "custom", 
		  "char_filter": ["my_mapping"],
	          "tokenizer": "standard",
	          "filter": ["lowercase"]
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
	      			}
	      		},
	      		"analyzer": {
	        		"my_analyzer": {
	          			"type": "custom", 
		  				"char_filter": ["my_mapping"],
	          			"tokenizer": "standard",
	          			"filter": ["lowercase", "myGreekLowerCaseFilter"]
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