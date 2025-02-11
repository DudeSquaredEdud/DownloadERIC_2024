#!/bin/sh
# 
# This is a download tool to get ERIC queries quickly.
# To use it, obtain a query URL from the ERIC api page and replace the "start=2000" with ${double}
# Use that to replace the curl URL and run the file.
#
# Please check the first query you download to see the total number of files present.
# Divide that number by 2000, and set it to the second number in the seq command below.
# It will allow you to download all files in that query..
#
# Thank you.
# 
for i in `seq 0 255`
do
  double=$((i*2))
  curl -X GET "https://api.ies.ed.gov/eric/?search=e_fulltextauth%3A%201%20OR%20e_fulltextauth%200&start=${double}000&rows=2000" -H "accept: */*" >> ${i}.json

done
