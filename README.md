# NOTICE

I am looking for universities and institutions outside of the US to hold the data as a way to preserve it. Please contact me if you would like to have a copy.

# Download ERIC

Originally just to download the documents from 2024 and 2025, extended to download all documents on the site.
This is to preserve the ERIC database in case any thing happens to the website.


# Usage

In the `ids` folder, you will find a file called `download.sh`. 

Construct a query using the ERIC API page, and submit at least one query request on the site to copy the `numFound` section. Divide this by 2000 and round down. This is the number of requests you will send. Input it as the second number in the `seq` command.  
Going back to the page, copy the API request and substitute it for the one that's there. Replace the "2" after `start=` with `${double}`. 
Please remember to include the ` >> ${i}.json ` at the end of it so the output goes into files.

