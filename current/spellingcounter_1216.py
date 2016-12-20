import time
import enchant
import codecs
import os
import clustertools as ct
import re
import string

##helper func
def spellchecker(word):
    americandict = enchant.Dict("en_US")
    result=americandict.check(word)
    return result


def spellingcounter(input_dir):
    """
    The spellingcounter counts the number of mis-spelled words.
    It uses the PyEnchange library for spellchecking.
    It iterates over the files in input_dir.
    It returns a lists of lists with (raw count, relative count) tuples.
    """
    start=time.time()
    goodwords=set(["wo", "'ve", "'m", "n't", "'s", "'ll"]+list(string.punctuation))
    htmlregex=re.compile("<.*?>")
    results=[]
    for pati in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
        print pati
        for fili in [i for i in os.listdir(os.path.join(input_dir, pati)) if not i.startswith(".")][:200]:
            print fili
            result=[]
            fili=codecs.open(os.path.join(input_dir, pati, fili), "r", "utf-8")
            inputad=ct.adtextextractor(fili.read(), fili)
            inputad=htmlregex.sub(" ", inputad)
            words=ct.tokenizer(inputad)
            #print "\n\n\n", words
            wordcount=float(len(words))
            mistakes=[w for w in words if not spellchecker(w) and w not in goodwords]
            #print result, len(result)
            if wordcount-len(mistakes) < 0:
                 print "WARNING: negative count-mistakes", wordcount, len(correct), os.path.join(input_dir, pati, fili)
            results.append([(len(mistakes), len(mistakes)/wordcount)])
            #print "\n".join([":".join([i, str(dict[i])]) for i in sorted(dict, key=dict.get, reverse=True)])
    end=time.time()
    print "len results", len(results)
    print "this took us {} minutes".format((end-start)/60)
    print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
    #for u in [[x[1] for x in i] for i in results]:
    #    print u
    print [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]
    return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]


spellingcounter("E:\cygwin\home\ps22344\Downloads\craig_0208")
