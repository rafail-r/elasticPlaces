#!/bin/bash

> elasticlogs.txt
> river_results.txt

realsize=0

for size in 1000 49000 50000 150000 250000 500000 9000000;
do
	realsize=$((size+realsize))
	echo "Testing "$realsize"" >> river_results.txt
	
	python ~/Desktop/webapp/ElasticPlaces/elasticsearch\ examples/gen.py $size
	
	for i in `seq 1 10`;
	do
		sleep 20
		> elasticlogs.txt
		python ~/Desktop/webapp/ElasticPlaces/elasticsearch\ examples/index.py
		sleep 45
		curl -XPUT "localhost:9200/_river/es_river/_meta" -d'{
			"type": "mongodb",
			"mongodb": {
				"db": "elasticPlaces", 
				"collection": "places",
				"options": {
					"include_fields": ["_id", "name", "formatted_address", "types", "geometry", "rating"]
				}
		    	},
			"index": {
				"name": "elasticplaces", 
				"type": "places"
			}
		}'
		sleep 25
		until grep -q "Number of documents indexed in initial import" elasticlogs.txt;
		do
			sleep 2
		done

		starttime=$(grep "MongoDBRiver is beginning initial import" elasticlogs.txt | grep -o '........,...' | tr -d ':' | tr -d ',')
		endtime=$(grep "Number of documents indexed in initial import" elasticlogs.txt | grep -o '........,...' | tr -d ':' | tr -d ',')


		echo "$starttime - $endtime" >> river_results.txt
		curl -XDELETE 'http://localhost:9200/_river/'
		sleep 30
	done
done
