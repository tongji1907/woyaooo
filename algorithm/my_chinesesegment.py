# -*- coding: utf-8 -*-
import datetime
import time
import fileinput
import string
import os
from operator import itemgetter
import math
import ictclas50
from ctypes import *

USEALL = True

#fstop = open("d:\\converse\\stopwords-utf8.txt","r")
stopwords = dict()
#for oneword in fstop.readlines():
#    try:
#        theword = unicode(oneword.strip(),"utf8")
#        stopwords[theword]= True
#    except:'
#        pass
#fstop.close()

for oneword in ['、','“','”','，','。','《','》','：','：','；','；','!','‘','’','?','？','！','·',' ','','】','(','（',')','）','.']:
    stopwords[oneword]= True


class ICTCLASException(Exception):
	def __init__(self, str_err):
		self.str_err = str_err

	def __str__(self):
		return self.str_err
'''
class Result(Structure):
	_fields_ = [("start", c_int),
			("length", c_int),
			("sPOS", c_char*8),
			("iPOS", c_int),
			("word_id", c_int),
			("word_type", c_int),
			("weight", c_int)]
'''
class ICTCLAS:

	def __init__(self):
                #self.ict = ictclass50
		#self.ict = CDLL(".//API2//libICTCLAS50.so")
 		#self.ict = ictclas50.ict_init("./API")		
		#if not self.ict.ICTCLAS_Init('.//API2'):
		if not  ictclas50.ict_init("./API"):		
			raise ICTCLASException,  "ictclas init failed"
		#if USEALL:
		#	t = self.ict.ICTCLAS_ImportUserDictFile(".//API2//alluserdict.txt",c_int(3))
		#else:
		#	t = self.ict.ICTCLAS_ImportUserDictFile(".//API2//userdict.txt",c_int(3))
		print "ictclas init succeed" #+ str( t)

	def __del__(self):
		#self.ict.ICTCLAS_Exit()
                ictclas50.ict_exit()
		pass

	def process_str(self, s):	
		len_s = len(s)          
		ret = []      
		li = ictclas50.process_str_a(s,len_s,ictclas50.codeType.utf8,False)
                for i in li:
			ret.append(s[i.startPos:(i.startPos+i.length)])
		#chinesestr[i.startPos:(i.startPos+i.length)]
		return ret
		#ch_addr = self.ict.ICTCLAS_ParagraphProcess(s)
		#return c_char_p(ch_addr).value


'''
	def process_str_result(self, text):
##		count = c_int()
##		addr = self.ict.ICTCLAS_ParagraphProcessA(s, byref(count))
##		r_list = (Result*count.value).from_address(addr)
		strlen = len(c_char_p(text).value)
		t = c_buffer(strlen*6)
		a =self.ict.ICTCLAS_ParagraphProcess(c_char_p(text),c_int(strlen),t,c_int(3),0)
		atext_list=t.value.split(' ')
		return atext_list

	def process_str_subject(self, s):
		count = c_int()
		addr = self.ict.ICTCLAS_ParagraphProcessA(s, byref(count))
		r_list = (Result*count.value).from_address(addr)
		count2 = c_int()
		self.ict.ICTCLAS_KeyWord(r_list, byref(count2))
		return r_list

	def process_str_finger(self, s):
		count = c_int()
		addr = self.ict.ICTCLAS_ParagraphProcessA(s, byref(count))
		return self.ict.ICTCLAS_FingerPrint()
'''				

'''
def loaduserwords():
    try:
        f= open("d:\\converse\\userwords.txt","r")
        lines = f.readlines()
        f.close()
        for oneline in lines:
            segmenter.adduserword(oneline.strip())
    except:
        pass
segmenter =ICTCLAS()
##loaduserwords()
'''

segmenter =ICTCLAS()
def splitchinese( t ,removenoisyword=True ):
    #t= t.lower().replace(" ","")+" "
    ret = []
    try:
        results = segmenter.process_str(t)
        for i in range(len(results)):
            curword = results[i]
            if removenoisyword and stopwords.has_key(curword ) :
                continue
            else:
                ret.append( curword)
    except Exception,err:
        print "segmentchinese error: "  + err.message+ t
    return ret

def loadsougouDic():
	f = open('.//Freq//SogouLabDic.dic')
        lines = f.readlines()
        f.close()   
        ret = dict()
        for line in lines:
	    values = line.split()
 	    #print (long(values[1]))
	    #s = unicode(values[0],"utf-8").encode("gb2312")
	    #print s
	    #print values[0].decode("gbk","ignore").encode("utf8")
            ret[values[0].decode("gbk","ignore").encode("utf8")] =int(values[1])
		 
	return ret

if __name__ == '__main__':
	
##	theall = open("API\\alluserdict.txt","w")
##	thefilepath = "API\\"
##	filenames = os.listdir(thefilepath)
##	for filename in filenames:
##		if filename.startswith("sogou"):
##			thefile = open(thefilepath + filename,"r")
##			filecontent = thefile.readlines()
##			for one in filecontent:
##				if len(one.strip()) >0:
##					theall.write(one.strip() +"\n")
##			thefile.close()
##	theall.close()
##
##    print thefilepath
##    for filename in filenames: 
	freqDic = loadsougouDic()
        print len(freqDic)	
	print "<sougou互联网词库> 加载完毕！"        
	#print freqDic[('凤凰')]
	text="我18.。。上班啦。。。朝阳哒。。。三元桥。。。哈。。。找一个踏踏实实在一起哒。。。好好过日子就哦啦。。。加我Q传照片给你。。。Q874419414.。。"
	segments  = splitchinese(text)
        segments_freq = dict()
	for segment in segments:
		try:
			if freqDic.has_key(segment):				
				if not (segments_freq.has_key(segment)):
					segments_freq[segment] = int(freqDic[segment])
			#print "#",unicode(one,"utf-8").encode("gb2312")
		except:
			print "decode error"
	#sorted(segments_freq.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        #[v for v in sorted(segments_freq.values())]
	segments_freq =sorted(segments_freq.items(), key=lambda segments_freq:segments_freq[1]) 
    	#print segments_freq
	for segment,freq in segments_freq:
		print  segment+'['+str(freq)+']'


    
