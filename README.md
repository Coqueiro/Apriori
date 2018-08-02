Python Implementation of Apriori Algorithm 
==========================================

This is an upgrade on the work done by [stdiff](https://github.com/stdiff/Apriori), which is an adaptation to Python3 from [asaini](https://github.com/asaini/Apriori)'s Python2 code, which attempts to implement the following paper:

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

The default hyperparameter values are *minSupport* = 0.15, *minConfidence* = 0.6, *minLift* = 1 and *minConviction* = 1

**CLI:**

To run the program inside CLI with dataset provided:

    python apriori.py -f INTEGRATED-DATASET.csv

To run program with dataset  

    python apriori.py -f INTEGRATED-DATASET.csv -s 0.17 -c 0.68 -l 1.5 -cv 1.2 -o lift

**Run inside code:**

To run program inside code with any other dataset:

    import apriori
    items, rules = apriori.runApriori(array_of_lists, minSupport = 0.15, minConfidence = 0.6, minLift = 1, minConviction = 1)
    apriori.printResults(items, rules, order = 'confidence')

**Recommendations:**

Best results are obtained for the following values:  

Support     : Between 0.1 and 0.2  

Confidence  : Between 0.5 and 0.7

Lift     : More than 1.0 for positive correlation.

Conviction  : More than 1.0 for positive correlation.

But this of course varies depending on the problem.

License
-------
MIT-License

-------
