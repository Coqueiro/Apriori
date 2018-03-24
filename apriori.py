#!/usr/bin/python3 
"""
Description     : Simple Python implementation of the Apriori Algorithm

Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence

    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import sys
import csv

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser


def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """calculates the support for items in the itemSet and returns a subset
    of the itemSet each of whose elements satisfies the minimum support"""
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count)/len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set([i.union(j) for i in itemSet for j in itemSet 
                if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, transactionList

def runApriori(data_iter, minSupport, minConfidence = 0.6, minLift = 1, minConviction = 1):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence, lift, conviction)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
            """local function which Returns the support of an item"""
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []

    for key, value in largeSet.items():
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    lift = getSupport(item)/(getSupport(element)*getSupport(remain))
                    conviction = (1-getSupport(remain))/(1-confidence)
                    if confidence >= minConfidence and lift >= minLift and conviction >= minConviction:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence, lift, conviction))
    return toRetItems, toRetRules


def printResults(items, rules, order):
    """
    prints the generated itemsets sorted by support and 
    the confidence rules sorted by confidence
    orders by confidence, lift or convinction
    """

    for item, support in sorted(items, key=lambda item: item[1]):
        print("item: %s \t %.3f" % (str(item), support))
    
    rule_key = 1
    if order == 'confidence': rule_key = 1
    elif order == 'lift': rule_key = 2
    elif order == 'conviction': rule_key = 3
        
    print('\n ------------------------ RULES:')
    print('\n ------- PRE \t POST \t CONFIDENCE \t LIFT \t CONVICTION -------\n')
    for rule, confidence, lift, conviction in sorted(rules, key=lambda rule: rule[rule_key]):
        pre, post = rule
        print("Rule: %s ==> \t %s \t %.3f \t %.3f \t %.3f" % (str(pre), str(post), confidence, lift, conviction))


def dataFromFile(fname, **kwargs):
    """Function which reads from the file and yields a generator"""

    with open(fname, 'r') as file_iter:
        reader = csv.reader(file_iter, delimiter=',')
        for line in reader:
            yield set(line)


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')
    optparser.add_option('-l', '--minLift',
                         dest='minL',
                         help='minimum lift value',
                         default=1,
                         type='float')
    optparser.add_option('-cv', '--minConviction',
                         dest='minCV',
                         help='minimum conviction value',
                         default=1,
                         type='float')
    optparser.add_option('-o', '--order',
                         dest='order',
                         help='order rule results by measure of interestingness',
                         default='confidence')

    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print('No dataset filename specified, system with exit')
        sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC
    minLift = options.minL
    minConviction = options.minCV
    order = options.order

    items, rules = runApriori(inFile, minSupport, minConfidence, minLift, minConviction)

    printResults(items, rules, order)

