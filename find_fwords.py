
def extractType(line):

    resultlist = []

    sw = line.split('|')
    for s in sw:
        if s != sw[0] and s != sw[1] and s != sw[2]:
            slist = s.split('\t')
            result = slist[len(slist) - 1].strip()
	    resultlist.append(result)

    return resultlist


def createLexs(flist):

    #Create two dicts
    cc_bliss = {}
    cc_swe = {}
    cc_aras = {}

    for line in flist:
        line = line.strip()
        if line != '':
            things = line.split('\t')
            cc = things[0].split('||')[0].strip()

            #Swedish word(s)
            if things[1] == '6,0 | 6':
                swedish = extractType(line)
                if cc_swe.has_key(cc):
                    cc_swe[cc].append(swedish)
                else:
                    cc_swe[cc] = [swedish]


            #Bliss file(s)
            if things[1] == '5,0 | 5':
                bliss = extractType(line)
                if cc_bliss.has_key(cc):
                    cc_bliss[cc].append(bliss)
                else:
                    cc_bliss[cc] = [bliss]

	    #Aras file(s)
            if things[1] == '20,0 | 20':
                aras = extractType(line)
                if cc_aras.has_key(cc):
                    cc_aras[cc].append(aras)
                else:
                    cc_aras[cc] = [aras]

    return cc_swe, cc_bliss, cc_aras



def matchTypes(cc_swe, cc_bliss, cc_aras):

    swe_bliss = {}
    swe_aras = {}

    for k in cc_swe.keys():
	swevalue = []
	for x in cc_swe[k]:
		for y in x:
			swevalue.append(y)

        if cc_bliss.has_key(k):
	    blissvalue = []
	    for x in cc_bliss[k]:
		for y in x:
			blissvalue.append(y)

            for i in swevalue:
                if swe_bliss.has_key(i):
                    for b in blissvalue:
                        swe_bliss[i].append(b)
                else:
                    swe_bliss[i] = []
                    for b in blissvalue:
                        swe_bliss[i].append(b)


        if cc_aras.has_key(k):
	    arasvalue = []
	    for x in cc_aras[k]:
		for y in x:
			arasvalue.append(y)

            for i in swevalue:
                if swe_aras.has_key(i):
                    for b in arasvalue:
                        swe_aras[i].append(b)
                else:
                    swe_aras[i] = []
                    for b in arasvalue:
                        swe_aras[i].append(b)


    return swe_bliss, swe_aras


flist = open('merged_cro_120702.txt', 'r')
swelex, blisslex, araslex = createLexs(flist)
swebliss, swearas = matchTypes(swelex, blisslex, araslex)

def wordToBliss(word):
    return swebliss.get(word)

if __name__ == "__main__":

    wordlist = ['hur.vb.01', 'var.vb.01', 'mig.nn.03', 'sig.pnm.02', 'eller.prep.02', 'endera.vb.01']



#OBS! For the Wordnet-CCF look-up, perhaps it would be better if we used my files as a lexicon instead, looking for wordnet index nr and extracting the ccf?

