#!/bin/bash

> python_results.txt
> java_results.txt

realsize=0
for size in 1000 49000 50000 150000 250000 500000 9000000;
do
	realsize=$((size+realsize))
	echo "Testing "$realsize"" >> python_results.txt
	echo "Testing "$realsize"" >> java_results.txt
	python ~/Desktop/elasticplaces/elasticsearch\ examples/gen.py $size
	sleep 2
	for i in `seq 1 10`;
	do
		python ~/index.py
		sleep 2
		{ time python ~/python_sync.py ; } 2>> python_results.txt
		sleep 2
		python ~/index.py
		sleep 2
		{ time java -jar ~/java_sync.jar ; } 2>> java_results.txt
		sleep 2
	done
done
