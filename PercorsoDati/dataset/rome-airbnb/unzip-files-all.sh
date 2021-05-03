#!/bin/bash

[[ -f reviews.csv.gz ]] || wget http://data.insideairbnb.com/italy/lazio/rome/2021-02-10/data/reviews.csv.gz
 wget http://data.insideairbnb.com/italy/lazio/rome/2021-02-10/data/calendar.csv.gz
 wget http://data.insideairbnb.com/italy/lazio/rome/2021-02-10/data/listings.csv.gz

gzip -d *.csv.gz

calendar.csv > calendar_complete.csv
reviews.csv > reviews_complete.csv
listings.csv > listings_complete.csv


