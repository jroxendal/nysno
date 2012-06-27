from urllib2 import urlopen
from urllib import urlencode
import json
import cPickle as pickle
from time import time
import sys
import traceback
from pprint import pprint
import nltk

from itertools import *
from collections import defaultdict, Counter

 


def fetchCorpus(num_sentences=0):
    data = {
        "corpus" : "ATTASIDOR",
        "cqp" : "<sentence> []",
        "start" : 0,
        "end" : num_sentences if num_sentences < 1000 else 999,
        "show" : "pos,lex,prefix,suffix,msd"
    }
    
    output = []
    exit = False
    kwic = []
    while True:
        result = json.load(urlopen("http://spraakbanken.gu.se/ws/korp", urlencode(data)))
        kwic = result["kwic"]
        if not kwic: break
        output.extend(kwic)
        data["start"] += 999
        data["end"] += 999
        if exit: break
        if num_sentences and data["end"] > num_sentences:
            data["end"] = num_sentences - 2
            exit = True
             
    return output
    
    # pickle.dump(output, open("kwic.pickle", "w"))
    

def countAmbiguities(tokens):
    d = defaultdict(Counter)
    
    for token in tokens:
        d[token["word"]].update(token["lex"].strip("|").split("|"))
    
    print "ambiguous:", map(lambda x: len(x) > 1, d.values()).count(True)
    print "not:", map(lambda x: len(x) > 1, d.values()).count(False)


if __name__ == '__main__':
    corpus = fetchCorpus(100)
    
    tokens = chain.from_iterable(map(lambda x: x["tokens"], corpus))
    
    d = imap(lambda x: (x["msd"], x["word"]), tokens)
    
    for msd, word in d:
        if msd.startswith("PM"):
            print word
    
    # d = imap(lambda x: (x["lex"], x["word"], x["prefix"], x["suffix"]), tokens)
    # print [x for x in d if x[2].strip("|") or x[3].strip("|")] 
    # isAmbiguous = lambda tup: len(tup[0].strip("|").split("|")) > 1
    
    # amb = ifilter(isAmbiguous, d)
    # fd = nltk.FreqDist(amb)
    
    
    
    # pprint([" ".join(k) + " " + str(v) for k,v in fd.items()])
    
    # for (lemgrams, word), v in fd.items():
        # print "%s:" % word
        # print "\n".join(lemgrams.strip("|").split("|"))
        # print 
    
    # pprint(map(lambda x: (x["word"], x["lex"]), corpus.tokens))
    
    
    
    
    
    