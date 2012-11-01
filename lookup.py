# encoding: utf-8
#from xml.etree import ElementTree as etree
from __future__ import unicode_literals
from lxml import etree
import json
from pprint import pprint
from urllib2 import urlopen
from itertools import chain, imap, ifilter
doc = etree.parse(open("wordnet.xml")).getroot()
mapping = {}
for sense in doc.getiterator("Sense"):
    formRepresentations = sense.getparent().xpath("./Lemma/FormRepresentation/feat[@att='synset']")
    mapping[sense.get("id")] = map(lambda x: x.get("val").split("%")[0], formRepresentations)

def getSynset(saldoid):
    return mapping[saldoid]

def getSynsetSafe(lemgramid):
    try:
        wd, _, _, n = lemgramid.split(".")
        synset = getSynset("%s..%s" % (wd, n))
        return synset 
    except:
        return None
        
if __name__ == '__main__':
#    output = urlopen("http://spraakbanken.gu.se/ws/korp?" +
#                         "corpus=ATTASIDOR&command=query&cqp=[lbound(sentence)]&start=0&end=999" +
#                         "&show=pos,msd,lex,prefix,suffix&defaultcontext=1%20sentence").read()
    output = urlopen("http://sve40.svenska.gu.se/cgi-bin/korp.cgi?" +
                         "corpus=NYSNO&command=query&cqp=[lbound(sentence)]&start=0&end=999" +
                         "&show=pos,msd,lemgram,prefix,suffix&defaultcontext=1%20sentence").read()
    
    from nysno_server import getBliss
                         
    output = json.loads(output)
    for struct in output["kwic"]:
        for token in struct["tokens"]:
            for attr in ["lemgram", "prefix", "suffix"]:
                saldolist = filter(bool, token[attr].split("|")) 
                wordnetlist = map(getSynsetSafe, saldolist)
                wordnetlist = list(chain.from_iterable(ifilter(bool, wordnetlist)))
                blisslist = map(getBliss, wordnetlist)
                blisslist = list(chain.from_iterable(ifilter(bool, blisslist)))
                
                if attr in ["prefix", "suffix"] and saldolist:
                    print " ".join(saldolist), wordnetlist, blisslist 
                    
                token[attr] = blisslist
    
    
    pprint (output) 
    