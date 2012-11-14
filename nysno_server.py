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
client = CCFClient("ccf.femtioprocent.com", 8899)


def getBliss(wd):
    req = {"Q":"lookup",
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
                saldolist = ifilter(bool, token[attr].split("|"))
                wordnetlist = imap(getSynsetSafe, saldolist)
                wordnetlist = chain.from_iterable(ifilter(bool, wordnetlist))
                blisslist = imap(getBliss, wordnetlist)
                blisslist = chain.from_iterable(ifilter(bool, blisslist))
                
                token[attr] = list(blisslist)
    return result


def blissMixin(data):
    return parseKorpResult(data)



def application(environ, start_response):
    
    try:
        input = environ["wsgi.input"].read(int(environ["CONTENT_LENGTH"]))
        environ["wsgi.input"] = StringIO(input)
    except KeyError:
        input = None
    data = json.loads(unquote(input))
    output = blissMixin(data)
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
