
def extractType(line):

    sw = line.split('|')
    for s in sw:
        if s != sw[0] and s != sw[1] and s != sw[2]:
            slist = s.split('\t')
            result = slist[len(slist) - 1].strip()

    return result


def createLexs(flist):

    #Create two dicts
    cc_bliss = {}
    cc_swe = {}

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

    return cc_swe, cc_bliss



def matchTypes(cc_swe, cc_bliss):

    swe_bliss = {}

    for k in cc_swe.keys():
        swevalue = cc_swe[k]

        if cc_bliss.has_key(k):
            blissvalue = cc_bliss[k]

            for i in swevalue:
                if swe_bliss.has_key(i):
                    for b in blissvalue:
                        swe_bliss[i].append(b)
                else:
                    swe_bliss[i] = []
                    for b in blissvalue:
                        swe_bliss[i].append(b)


    return swe_bliss


flist = open('merged_cro_120702.txt', 'r')
swelex, blisslex = createLexs(flist)
swebliss = matchTypes(swelex, blisslex)
print swebliss
def wordToBliss(word):
    return swebliss.get(word)

if __name__ == "__main__":

    wordlist = ['hur.vb.01', 'var.vb.01', 'mig.nn.03', 'sig.pnm.02', 'eller.prep.02', 'endera.vb.01']



#OBS! For the Wordnet-CCF look-up, perhaps it would be better if we used my files as a lexicon instead, looking for wordnet index nr and extracting the ccf?

