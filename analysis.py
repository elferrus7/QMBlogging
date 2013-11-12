from __future__ import print_function
from alchemyapi import AlchemyAPI
import abc
import json
#Imports for Bitext
import httplib, urllib

#Imports for Alchemiyst

class Analysis(object):
    __metaclass__ = abc.ABCMeta
    
    lang = ''
    server = ''
    
    def __init__(self,lang,server):
        self.lang = lang
        self.server = server
        
    def connect(self):
        raise NotImplementedError
    
    def count_repetitions(self):
        raise NotImplementedError
    
    def get_entities(self):
        raise NotImplementedError
        
    def get_sentiment(self):
        raise NotImplementedError
    
class Bitext(Analysis):
    
    service='/WS_Nops_Val/Service.aspx'
    
    def __init__(self,lang,server,usr,pwd):
        self.lang = lang
        self.server = server
        self.usr = usr
        self.pwd = pwd
        
    def get_entities(self,txt):
        id = '0001'
        params = urllib.urlencode({'User': '%s' % self.usr, 'Pass': '%s' %self.pwd, 'Lang': '%s' % self.lang, 'ID': '%s' %id, 'Text': '%s' % txt, 'Detail': 'Detailed', 'OutFormat':'JSON', 'Normalized': 'No', 'Theme': 'Gen'})

        # HTML headers required
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        
        # Server. In case of need, please check with Bitext for an updatged list of available servers
        #server="svc8.bitext.com"
        
        # The POST
        conn = httplib.HTTPConnection("%s" % self.server)
        conn.request("POST", "%s" % self.service, params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        
        #print data

class Alchemy(Analysis):
    
    
    def __init__(self):
        self.alchemyapi = AlchemyAPI()
        
    def get_entities(self,txt):
        print('Processing text: ', txt)
        print('')
        
        response = self.alchemyapi.entities('text',txt)
        
        if response['status'] == 'OK':
            print('')
            print('## Entities ##')
            for entity in response['entities']:
                print('text: ', entity['text'])
                print('type: ', entity['type'])
                print('relevance: ', entity['relevance'])
                print('')
        else:
            print('Error in entity extraction call: ', response['statusInfo'])

    def get_sentiment(self,txt):
        response = self.alchemyapi.sentiment('text',txt)
        
        if response['status'] == 'OK':
            print('## Response Object ##')
            print(json.dumps(response, indent=4))
         
            print('')
            print('## Document Sentiment ##')
            print('type: ', response['docSentiment']['type'])
            print('score: ', response['docSentiment']['score'])
        else:
            print('Error in sentiment analysis call: ', response['statusInfo'])
        
# bit = Bitext('eng','svc8.bitext.com','elferrus7','mmohuevos7')
# bit.get_entities(txt='All our growth is organic we didnt spend money on advertising is the new the market is so big that we only need to take 1 badpitch')

# alchemy = Alchemy()
# alchemy.get_entities(txt='Yesterday dumb Bob destroyed my fancy iPhone in beautiful Denver, Colorado. I guess I will have to head over to the Apple Store and buy a new one.')