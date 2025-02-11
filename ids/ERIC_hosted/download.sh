#!/bin/sh
for i in `seq 0 25`
do
  double=i*2
  curl -X GET "https://api.ies.ed.gov/eric/?search=e_fulltextauth%3A%201&start=${double}000&rows=2000&fields=id%20title" -H "accept: */*" >> ${i}.json

done
