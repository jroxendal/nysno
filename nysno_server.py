#!/usr/bin/python
from wsgiref.simple_server import make_server
import os
import subprocess
import traceback, sys
from urllib2 import urlopen
import cgi
import urllib, json
from itertools import chain, imap, ifilter

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
    struct = {"arr" : {"repr" : "fel"}}
    return [x["repr"].split("/")[-1] for x in struct["arr"] if x["repr"]]


def parseKorpResult(result):
    output = json.loads(result)
    for struct in output["kwic"]:
        for token in struct["tokens"]:
            for attr in ["lemgram", "prefix", "suffix"]:
                saldolist = ifilter(bool, token[attr].split("|")) 
                wordnetlist = imap(getSynsetSafe, saldolist)
                wordnetlist = chain.from_iterable(ifilter(bool, wordnetlist))
                blisslist = imap(getBliss, wordnetlist)
                blisslist = chain.from_iterable(ifilter(bool, blisslist))
                
                token[attr] = list(blisslist)
    return output


def pipeline(environ, start_response):
    
    # try:
        # input = environ["wsgi.input"].read(environ["CONTENT_LENGTH"])
        # environ["wsgi.input"] = StringIO(input)
    # except KeyError:
        # input = None
    data = {}
    if "QUERY_STRING" in environ and environ["QUERY_STRING"]:
        data.update(x.split("=") for x in environ["QUERY_STRING"].split("&"))
    
    try:
        # make vrt from input
        subprocess.check_call(["make", "distclean"])
        f = open("nysno/nysno.xml", "w")
        f.write("<text>%s</text>" % urllib.unquote_plus(data["text"]))
        f.close()
        subprocess.check_call(["make", "vrt"])
        
        # remove old corpus
        try:
            subprocess.check_call(["rm", "-r", "/corpora/data/nysno/*"])
        except:
            pass
        # import vrt into cwb
        subprocess.check_call([
                               "/usr/local/cwb-3.4.4/bin/cwb-encode",
                                "-s", "-p", "-", "-d", "/corpora/data/nysno",
                                 "-R", "/corpora/registry/nysno", "-c", "utf8",
                                  "-f", "annotations/nysno.vrt", "-P", "word", 
                                  "-P", "pos", "-S", "sentence:0+id", 
                                  "-P", "msd",  
                                  "-P", "lemgram",  
                                  "-P", "prefix",  
                                  "-P", "suffix",  
                               ])
        subprocess.check_call(["/usr/local/cwb-3.4.4/bin/cwb-makeall", "-V", "-r", "/corpora/registry", "NYSNO"])
        
        # get json result
        output = urlopen("http://localhost/cgi-bin/korp.cgi?" +
                         "corpus=NYSNO&command=query&cqp=[lbound(sentence)]&start=0&end=999" +
                         "&show=pos,msd,lemgram,prefix,suffix&defaultcontext=1%20sentence").read()
        
        output = parseKorpResult(output)
        
        status = '200 OK'
        headers = [('Content-type', 'application/json'), ("Access-Control-Allow-Origin", "*")]
        start_response(status, headers)
        return [json.dumps(output)]
    except Exception, e:
        status = '403 FORBIDDEN'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [traceback.format_exc()]
        
    
    
if __name__ == '__main__':
    httpd = make_server('ubuntu.local', 8000, pipeline)
    print "Serving on port 8000..."
    httpd.serve_forever()