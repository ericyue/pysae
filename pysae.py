#
# pysae v0.1
# sina app engine python sdk (not official)
# author : Eric Yue  (http://weibo.com/ericyue)
# blog   : www.ericyue.info
# email  : hi.moonlight@gmail.com
#
# NOW,ONLY SUPPORT "SEGMENT" AND "SMS"
#
import json
import time
import hmac
import base64
import pycurl
import hashlib
import urllib
import sys

#SUPPORT CHINESE
reload(sys)
sys.setdefaultencoding('utf-8')

class SAE_APIBus(object):
    
    def __init__(self,accesskey,secretkey):
        self.end= "http://g.apibus.io"
        self.accesskey=accesskey
        self.secretkey=secretkey
    
    def writeBody(self,content):
        self.body=content
        return len(self.body)
    
    def writeHeader(self,content):
        self.header=content
        return len(self.header)

    def signature(self,timestamp):
        content="FetchUrl"+self.url+"TimeStamp"+str(timestamp)+"AccessKey"+self.accesskey
        sig=base64.b64encode(hmac.new(self.secretkey,content,hashlib.sha256).digest())
        return sig
  
    def load(self,service,word_tag=1):
        #
        #   SET THE SERVICE YOU WANT
        #   // when you use segment service,
        #   // you can specify the "word_tag" to show the word tag or not
        #   // find more: http://apidoc.sinaapp.com/sae/SaeSegment.html
        #   
        if service=='segment':
            #segment
            self.url = "http://segment.sae.sina.com.cn/urlclient.php?word_tag="+str(word_tag)+"&encoding=UTF-8"    
        elif service=='sms':
            #sms
            self.url="http://inno.smsinter.sina.com.cn/sae_sms_service/sendsms.php"

    def setSegmentContent(self,content):
        self.params={"context":content}
        self.params=urllib.urlencode(self.params)

    def setSMS(self,mobile,msg,encoding):
        self.params={"mobile":mobile,"msg":msg,"encoding":encoding}
        self.params=urllib.urlencode(self.params)

    def fetch(self,headers=None,callback=None):
        if self.params is None:
            print 'ERROR: SET THE PARAMS FIRST!'
            return None
        self.callback=callback
        timestamp=str(int(time.time()))
        sig=self.signature(timestamp)
        headers=["FetchUrl:"+self.url,"AccessKey:"+self.accesskey,"TimeStamp:"+timestamp,"Signature:"+sig]
        self.header=None
        self.body=None
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION, self.writeBody)
        c.setopt(pycurl.HEADERFUNCTION, self.writeHeader)
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.POSTFIELDS,self.params)
        c.setopt(pycurl.HTTPHEADER,headers)
        c.setopt(pycurl.URL, self.end)
        c.perform()
        return self.body

    



