#!/opt/local/bin/python2.5
# -*- coding: utf-8 -*-

from name_database import name_ident
import composition
import re, sys, string, cgi, time
from pprint import pprint
import urllib2
import xml.etree.ElementTree as etree


def getFreq(lst):
    dict1 = {}
    dict2 = {}
    
    for tup in lst:
        dict1[tup[0]] = (dict1[tup[0]]+1) if dict1.has_key(tup[0]) else 1
        dict2[tup[1]] = (dict2[tup[1]]+1) if dict2.has_key(tup[1]) else 1
        
    return (dict1, dict2)
    

def disambiguate(input, freqTable, struct):
    ''' Takes a lexem and return the corresponding lemma. 
    if more than one lemma is found it returns the most common one.
    '''
    
    def getLemma(lex, struct):
        output = []
        for tup in struct:
            if tup[0] == lex:
                output.append(tup)
        if len(output) == 0:
            return False
        return output

    
    lst = getLemma(input, struct) 
    
    if not lst:
        return False
    
    wordSet = set(lst)
    lemmaList = [y for x,y in list(wordSet)]
    def sortFunc(x, y):
        nX = freqTable[x]
        nY = freqTable[y]
        if nX > nY:
            return -1
        elif nX == nY:
            return 0
        else:
            return 1 
    
    lemmaList.sort(sortFunc)
    # return most frequent lemma
    # hack for ignoring ambiguous lemmas like the swedish "får"
    return [lemmaList[0]]
#    return lemmaList
        

def tokenize(input):
    stripped = ""
    output = []
    for char in input:
        if char not in "#$%&'()*+,-./:;=?@[\]^`{}~\"":
            stripped += char
    stripped = re.sub("\s+", " ", stripped)
            
    return stripped.split(" ")

def getLexicon():
    '''
    Fetches and parses the translation mapping. 
    '''
    lex = unicode(open("../resources/lemmata_mapping.txt", "r").read(), "utf8")
    lex = lex.splitlines()

    output = {}
    for elem in lex:
        line = elem.split("|")
        
        line = [x.strip() for x in line]
        if len(line) < 2:
            continue
        sweWordList = [x.strip() for x in line[2].split(",")]
        for sweWord in sweWordList:
            value = line[1]
            if not output.has_key(sweWord):
                output[sweWord] = set()
            output[sweWord].add(value)
            
    return output


def getImage(wordList, translateLex):
    '''
    Returns a list of file names corresponding to a list of lexems.
    If the requested lexem is not found, "UNKNOWN" is returned.  
    '''
    output = []
    for word in wordList:
        if translateLex.has_key(word):
            translated = list(translateLex[word])
            output.append(translated if len(translated) >1 else translated[0])
        else:
            output.append("UNKNOWN")
    return output

def tokenizeCorpus():
    data = unicode(open("../resources/8sidor2006tag_utf8.txt", "r").read(), "utf8")
    
    data = re.sub("\s+", " ", data)
    # split into tuples
    output = [tuple(x.split("/")) for x in data.split(" ")]
    # filter empty strings
    
    output = [x for x in output if len(x) == 2 and len(x[1]) > 0]
    return output
    
def printStats(lexList, lemmaList, result):
    
    print "Compositions:"
    print "Lexem         Result:"
    for lex, item in zip(lexList, result):
        if type(item) == tuple:
            print "" + lex + "       " + unicode(item)
             
    print "-"*60
    
    largeStruct = zip(lexList, lemmaList, result)
    print u"%-20s       %-20s       %-20s" % ("Lexem", "Lemma", "Filename")
    print "-"*60
    for lex, lemma, item in largeStruct:
        print u"%-20s       %-20s       %-20s" % (lex, lemma, item if type(item) != list else [str(x) for x in item])
    
    nKnown = len([x for x in result if x != "UNKNOWN" and x != "NAME_NOT_FOUND" and type(x) != tuple])

    nAmbiguous = len([x for x in result if (type(x) == list or type(x) == tuple) and len(x) > 1])
    nTotal = len(lexList)
    print "%% matches: %.2f whereof %.2f%% ambiguous" % (100*float(nKnown)/float(nTotal), 100*float(nAmbiguous)/float(nKnown))


def getCompImage(word, resultList, lexicon, cmpsr):
    '''
    Takes a word, a list of lemmas and a lexicon.
    returns a list of file names. The two parts of a composition 
    are stored as a tuple. Ambiguities are represented as a list.
    '''
    output = []
    imageList = getImage(resultList, lexicon)
    if imageList == ["UNKNOWN"]:
        return tuple(cmpsr.composition(word))
    return imageList
 

def getRemoteArticle(url):
    '''
    Fetches a remote article using http and returns the text with html
    stripped. Only to be used with 8sidor.se for the snigl application.  
    '''
    file = urllib2.urlopen(url).read()
    article = re.search(r"<h4>.*?</p>", file, re.DOTALL)
    article = re.sub(r"<.+?>", " ", article.group(0))
    return article

def getSynSet(fileName):
    '''@deprecated: moved to the front end
    Fetches the synset code for a given filename. 
    '''
    lex = unicode(open("../resources/lemmata_mapping.txt", "r").read(), "utf8")
    foundRow = re.findall(fileName + ".*", lex)
    return foundRow[0].split("|")[1].strip() if foundRow != [] else ""
    
    

def structToXML(struct):
    '''
    Ouputs the datamodel to an xml structure. 
    '''
    def makeTag(val, tagName):
        if "img" in tagName and re.search(r"\w+\.jpg|png", val) != None:
            tb.start(tagName, {"isName":"true"})
        elif "img" in tagName:
            tb.start(tagName, {"isName":"false"})
        else:
            tb.start(tagName, {})
            
            
        tb.data(val)
        tb.end(tagName)
    
    def makeTagList(lst, tagName="img"):
        if type(lst) == unicode or type(lst) == str:
            makeTag(lst, tagName)
        elif type(lst) == list:
            for elem in lst:
                makeTag(elem, tagName)
        elif type(lst) == tuple:
            makeTagList(lst[0])
            makeTagList(lst[1], "img_2")
        else:
            sys.exit("crash " + str(type(lst)))
            
    
    tb = etree.TreeBuilder()
    tb.start("tokens", {})

    for (word, seq) in struct:
        tokenTag = tb.start("token", {})
        makeTag(word, "word")
        
        makeTagList(seq)
        
        tb.end("token")
    
    
    tb.end("tokens")
    return tb.close()


def name_identifier(text):
    '''
    Takes an input text and and tags any real case word. 
    Two adjacent real cased words are joined by underscore, e.g.
    "Bill Clinton" is tagged "<Bill_Clinton>".
    '''
    
    #ms = re.finditer(ur"([^\.]\s)([A-Z\xc5\xc4\xd6]\w+( [A-Z\xc5\xc4\xd6]\w+)*)", text, re.UNICODE)
    #Sandra's code - works for all names in 'text', both with and without a point after the initial:    
    ms = re.finditer(ur"([A-Z\xc5\xc4\xd6]\w+( ([A-Z\xc5\xc4\xd6])*(\.)*(\s)*[A-Z\xc5\xc4\xd6]\w+)*)", text, re.UNICODE) 

    def replaceInSpan(newStr, (n, m), text):
        lst = list(text)
        lst[n:m] = newStr
        return "".join(lst)
    
    
    names = []
    spans = []
    for m in ms:
        #names.append(m.expand(r"<\2>").replace(" ", "_"))
        #spans.append(m.span(2))
        
        #Sandra's code, uses group 1, due to changed regexp (first part of my regexp):
        names.append(m.expand(r"<\1>").replace(" ", "_")) 
        spans.append(m.span(1))        
    
    names.reverse()
    spans.reverse()
    
    output = text
    for (newS, span) in zip(names, spans):
        output = replaceInSpan(newS, span, output)
    return output

 
def main():
    
    t1 = time.time()
    form = cgi.FieldStorage()
    if form.has_key("getURL"):
        print "Content-type:text/plain\n"
        print getRemoteArticle(form["getURL"].value)
        return
    
    testData = unicode(open("../resources/8_sidor_testcorpus.txt", "r").read(), "utf8")
    doCGI = False
    if form.has_key("data"):
        print "Content-type:text/xml\n"
        testData = unicode(form["data"].value, "utf8")
        doCGI = True
        
            
    # proper names are tagged
    testData = name_identifier(testData.strip()) 
    structure = tokenizeCorpus()
    lexicon = getLexicon()
    
    # assign value to global variables
    symbol_freq_dist, lemma_freq_dist = getFreq(structure)
    
    composer = composition.Composer(structure, lexicon, lemma_freq_dist)
    # test input
    stripped = tokenize(testData)
    
    output = []
    lemmaStruct = []
    
    isName = lambda x: x[0] == u"<" and x[-1] == u">"
    isAmbiguous = lambda x:type(x) == type([])    
    
    def makeFileList(word, lemmaList):
        # resultList: will contain the actual lemma representation
        resultList = []
        # the lemma is found    
        if lemmaList and not isAmbiguous(lemmaList):

            imageList = getCompImage(word, lemmaList, lexicon, composer)
        elif isAmbiguous(lemmaList):
            for lemma in lemmaList:
                resultList.append(lemma)
            imageList = getCompImage(word, resultList, lexicon, composer)
        # the lemma is not found
        else:
            resultList = ["UNKNOWN"]
            # assume unknown word is composition
            imageList = getCompImage(word, resultList, lexicon, composer)
        return (resultList, imageList)
    
    # proccess each word in the input to produce 
    # a matching file name.
    for word in stripped:
        if isName(word):
            imageList = name_ident(word.replace("_", " ")[1:-1])
            resultList = ["PN"] 
        else:
            lemmaList = disambiguate(word, lemma_freq_dist, structure)
            resultList, imageList = makeFileList(word, lemmaList)  
              
        lemmaStruct.append(resultList if len(resultList) > 1 else resultList[0])
        output.append(imageList if len(imageList) > 1 else imageList[0])
    # lists mark ambiguities.
    
    stripIfName = lambda x: re.sub("[<>]", "", x) if isName(x) else x
    stripped = [stripIfName(x) for x in stripped]
    
    if doCGI:
        
        xmlData = structToXML(zip(stripped, output))
        tree = etree.ElementTree(xmlData)
        print '<?xml version="1.0" ?>'
        print etree.tostring(tree.getroot())
    else:

        printStats(stripped, lemmaStruct, output)
        print "Execution time for the %s words: %.2f seconds" % (len(stripped), time.time() - t1)



if __name__ == "__main__":
    main()
    
