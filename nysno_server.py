#!/usr/bin/python
from wsgiref.simple_server import make_server
import os, json
import subprocess
import traceback, sys
from urllib2 import urlopen
import cgi
import urllib, json
from StringIO import StringIO
from itertools import chain, imap, ifilter
from urllib import unquote



from lookup import getSynsetSafe
from ccfconnect import CCFClient
client = CCFClient("ccf.conceptcoding.org", 8899)

from find_fwords import wordToBliss



def getBliss(wd):
    req = {"Q": "lookup",
       "ref":"REF",
       "seq":12345,
       "word": wd,
       "langIn":"en",
       "langOut":"bliss"}
    struct = client.get_json(req)
    return [x["repr"].split("/")[-1] for x in struct["arr"] if x["repr"]]


def parseKorpResult(result):
    # output = json.loads(result)
    for struct in result["kwic"]:
        for token in struct["tokens"]:
            for attr in ["lex", "prefix", "suffix"]:
                # get rid of emtpy sets
                saldolist   = filter(bool, token[attr].split("|"))
                # get list of wordnet identifiers for each lemgram
                wordnetlist = map(getSynsetSafe, saldolist)
                # get rid of empty and flatten list
                wordnetlist = list(chain.from_iterable(ifilter(bool, wordnetlist)))
                # for each wordnet identifier, get an image filname from the ccf server
                blisslist   = map(getBliss, wordnetlist)
                # get rid of empty and flatten
                blisslist   = list(chain.from_iterable(ifilter(bool, blisslist)))

                if not blisslist and saldolist:
                    wdlist = map(lambda x: x.split(".")[0], saldolist)
                    blisslist = map(wordToBliss, wdlist)


                token[attr] = blisslist
    return result


def blissMixin(data):
    return parseKorpResult(data)


def application(environ, start_response):
    form = cgi.FieldStorage(fp=environ["wsgi.input"],
                           environ=environ,
                           keep_blank_values=True)

    text = json.loads(form["text"].value)
    output = blissMixin(text)
    try:

        status = '200 OK'
        headers = [('Content-type', 'application/json'), ("Access-Control-Allow-Origin", "*")]
        start_response(status, headers)
        return [json.dumps(output)]
    except Exception, e:
        print "exception caught", e
        status = '403 FORBIDDEN'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [traceback.format_exc()]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print "Serving on port 8000..."
    httpd.serve_forever()
