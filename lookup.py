# encoding: utf-8
#from xml.etree import ElementTree as etree
from __future__ import unicode_literals
from lxml import etree
import json
from pprint import pprint
from urllib2 import urlopen
from itertools import chain, imap, ifilter
import os

path = os.path.dirname(__file__)


doc = etree.parse(open(path + "/wordnet.xml")).getroot()
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
    getSynset("lite..ab.1")    