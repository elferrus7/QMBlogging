import abc

import httplib, urllib

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
        
    def get_emotions(self):
        raise NotImplementedError
    
class Bitext(Analysis):
    
    service='/WS_Nops_Val/Service.aspx'
    
    def __init__(self,lang,server,usr,pwd):
        self.lang = lang
        self.server = server
        self.usr = usr
        self.pwd = pwd
        
    def get_entities(self,txt):
        #txt = 'The API is very good'
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
        
        print data
        
# bit = Bitext('eng','svc8.bitext.com','elferrus7','mmohuevos7')
# bit.get_entities(txt='The API is very good')