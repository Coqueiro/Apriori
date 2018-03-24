Python Implementation of Apriori Algorithm 
==========================================

[![Build Status](https://travis-ci.org/asaini/Apriori.svg?branch=master)](https://travis-ci.org/asaini/Apriori)

The code attempts to implement the following paper:

> *Agrawal, Rakesh, and Ramakrishnan Srikant. "Fast algorithms for mining association rules." Proc. 20th int. conf. very large data bases, VLDB. Vol. 1215. 1994.*

List of files
-------------
1. apriori.py
2. INTEGRATED-DATASET.csv
3. README(this file)

The dataset is a copy of the “Online directory of certified businesses with a detailed profile” file from the Small Business Services (SBS) 
dataset in the `NYC Open Data Sets <http://nycopendata.socrata.com/>`_

This version of the main repository adds the possibility of verifying Lift and Conviction, both measures of interestingness.

Usage
-----
To run the program with dataset provided and default values for *minSupport* = 0.15, *minConfidence* = 0.6, *minLift* = 1 and *minConviction* = 1

    python apriori.py -f INTEGRATED-DATASET.csv

To run program with dataset  

    python apriori.py -f INTEGRATED-DATASET.csv -s 0.17 -c 0.68 -l 1.5 -cv 1.2 -o lift

Best results are obtained for the following values:  

Support     : Between 0.1 and 0.2  

Confidence  : Between 0.5 and 0.7

Lift     : More than 1.0

Conviction  : More than 1.0

License
-------
MIT-License

-------
