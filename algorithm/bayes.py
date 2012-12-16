# -*- coding: utf-8 -*-
import math 
#import mylib
import zlib
mindistance = 0.01 # mininum

import data
import model
from model import conversation

from data import dbfactory
from model import doc
from model import talk
import my_chinesesegment

LN2 = math.log(2)



def chi2Q(x2, v, exp=math.exp, min=min):
    """Return prob(chisq >= x2, with v degrees of freedom).

    v must be even.
    """
    assert v & 1 == 0
    # XXX If x2 is very large, exp(-m) will underflow to 0.
    m = x2 / 2.0
    sum = term = exp(-m)
    for i in range(1, v//2):
        term *= m / i
        sum += term
    # With small x2 and large v, accumulated roundoff error, plus error in
    # the platform exp(), can cause this to spill a few ULP above 1.0.  For
    # example, chi2Q(100, 300) on my box has sum == 1.0 + 2.0**-52 at this
    # point.  Returning a value even a teensy bit over 1.0 is no good.
    return min(sum, 1.0)

class WordInfo(object):
    __slots__ = 'needcount', 'othercount'

    def __init__(self):
        self.__setstate__((0, 0))

    def __repr__(self):
        return "WordInfo" + repr((self.needcount, self.othercount))

    def __getstate__(self):
        return self.needcount, self.othercount

    def __setstate__(self, t):
        self.needcount, self.othercount = t


class Classifier:

    def __init__(self):
        self.wordinfo = {}
        self.nneed = self.nother = 0
        
    def reset(self):
        self.wordinfo = {}
        self.nneed = self.nother = 0
    def status(self):
        return " wordinfo " + str(len(self.wordinfo)) +" ����:" + str(self.nneed) +" ����:" + str(self.nother) 
        
    def needprobability(self, wordstream, evidence=False):
        from math import frexp, log as ln
        
        H = S = 1.0
        Hexp = Sexp = 0

        clues = self._getclues(wordstream)
        for prob, word, record in clues:
            S *= 1.0 - prob
            H *= prob
            if S < 1e-200:  # prevent underflow
                S, e = frexp(S)
                Sexp += e
            if H < 1e-200:  # prevent underflow
                H, e = frexp(H)
                Hexp += e

        # Compute the natural log of the product = sum of the logs:
        # ln(x * 2**i) = ln(x) + i * ln(2).
        S = ln(S) + Sexp * LN2
        H = ln(H) + Hexp * LN2

        n = len(clues)
        if n:
            S = 1.0 - chi2Q(-2.0 * S, 2*n)
            H = 1.0 - chi2Q(-2.0 * H, 2*n)

            prob = (S-H + 1.0) / 2.0
        else:
            prob = 0.5

        if evidence:
            clues = [(w, p) for p, w, r in clues]
            clues.sort(lambda a, b: cmp(a[1], b[1]))
            clues.insert(0, ('*S*', S))
            clues.insert(0, ('*H*', H))
            return prob, clues
        else:
            return prob



    def probability(self, record):
        needcount = record.needcount
        othercount = record.othercount

        nother = float(self.nother or 1)
        nneed = float(self.nneed or 1)

        assert othercount <= nother, "Token seen in more other than other trained."
        otherratio = othercount / nother

        assert needcount <= nneed, "Token seen in more need than need trained."
        needratio = needcount / nneed

        prob = needratio / (otherratio + needratio)
##        S = options["Classifier", "unknown_word_strength"]
##        StimesX = S * options["Classifier", "unknown_word_prob"]
        S = 1
        StimesX = 0.5
        n = othercount + needcount
        prob = (StimesX + n * prob) / (S + n)

        return prob
    
    def _getclues(self, wordstream):
        clues = []
        push = clues.append
        for word in set(wordstream):
            tup = self._worddistanceget(word)
            if tup[0] >= mindistance:
                push(tup)
        clues.sort()  # sort by distance
        return [t[1:] for t in clues]

    def _worddistanceget(self, word):
        record = self.wordinfo.get(word)
        if record is None:
            prob = 0.5
        else:
            prob = self.probability(record)
        distance = abs(prob - 0.5)
        return distance, prob, word, record    
        
    def learn(self, wordstream, is_need):
        if is_need:
            self.nneed += 1
        else:
            self.nother += 1

        for word in set(wordstream):
            record = self.wordinfo.get(word)
            if record is None:
                record = WordInfo()

            if is_need:
                record.needcount += 1
            else:
                record.othercount += 1

            self.wordinfo[word] = record

    def unlearn(self, wordstream, is_need):
        """In case of pilot error, call unlearn ASAP after screwing up.
        Pass the same arguments you passed to learn().
        """
        pass

def my_learnstore(is_need):
    engine =data.engine_from_config()
    db = data.init_datafactory(engine)
    talks = dbfactory.Session().query(talk.Talk).filter(intent>20)

    for item in talks:
        print item.description
        words = my_chinesesegment.splitchinese(item.description)
        mybayes.learn( words,is_need)

    pass

def learnstore( storename, is_need):
    '''
    needstore = mylib.Store(storename)
    rows = needstore.getbysql( " select object from rdfstore")

    for onerow in rows:
        try:
            theobject = eval(zlib.decompress(onerow[0]))
            words =  mylib.splitchinese(theobject["snippet"])
            mybayes.learn( words,is_need)
        except Exception,err:
            mylib.writelog(storename +  "learnstore error" + err.message,prefix="log\\bayes",file=True)
    '''
    pass
def learntalks( talks, is_need):
    '''
    for onetalk in talks:
        try:            
            words =  mylib.splitchinese(onetalk)
            mybayes.learn( words,is_need)
        except Exception,err:
            mylib.writelog(onetalk +  " learn error" + err.message,prefix="log\\bayes",file=True)
    '''
    pass

def my_relearn(focus = None,other = None):
    my_learnstore()
    print mybayes.status()

def relearn( focus = None , other = None):
    '''
    sstore = mylib.Store("system")
    if focus is None:
        focus = sstore.getattri("focustore","value")
        
    if other is None:
        other = sstore.getattri("otherstore","value")
        
    if focus is None:
        focus = "need"
        other ="service"

    mybayes.reset()
    print "bayes cleaned "
    focusss = focus.split()
    print "bayes focus :",focus
    for one in focusss:
        learnstore(  one.strip(),True)
    print "bayes other :",other
    othersss = other.split()
    for one in othersss:
        learnstore(  one.strip(),False)
    print mybayes.status()
    '''
    pass

def reset(  ):
    mybayes.reset()

def checkneedprobability( content ):
    global learned
    if learned == 1 :
        relearn()
        learned = 0
    wordsforlearn = my_chinesesegment.splitchinese(content)
    return mybayes.needprobability( wordsforlearn,evidence=False)
    #return mybayes.needprobability( mylib.splitchinese(content),evidence=False)

def status():
    return mybayes.status()

mybayes = Classifier()

learned = 1

if __name__ == '__main__':
    print checkneedprobability("我18.。。上班啦。。。朝阳哒。。。三元桥。。。哈。。。找一个踏踏实实在一起哒。。。好好过日子就哦啦。。。加我Q传照片给你。。。Q874419414.。。")
    print learned