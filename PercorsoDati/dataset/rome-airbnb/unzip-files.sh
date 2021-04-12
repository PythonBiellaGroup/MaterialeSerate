#!/bin/bash

[[ -f reviews.csv.gz ]] || wget http://data.insideairbnb.com/italy/lazio/rome/2021-02-10/data/reviews.csv.gz
 wget http://data.insideairbnb.com/italy/lazio/rome/2021-02-10/data/calendar.csv.gz
 wget http://data.insideairbnb.com/italy/lazio/rome/2021-02-10/data/listings.csv.gz

gzip -d *.csv.gz

head -n 10000 calendar.csv > calendar_sample.csv
head -n 10000 reviews.csv > reviews_sample.csv
head -n 10000 listings.csv > listings_sample.csv


