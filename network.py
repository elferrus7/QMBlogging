#Imports for Network class
import abc 

#Twitter specific imports
import twitter
#Network class is an interface to acces to all the methods for mining the network

class Network(object):
    __metaclass__ = abc.ABCMeta
            
    @abc.abstractmethod    
    def login(self):
        raise NotImplementedError
    
    def get_top(self):
        raise NotImplementedError
    
    def get_by_dates(self,date_from,date_to):
        raise NotImplementedError
    
    def get_by_location(self,location):
        raise NotImplementedError
    
class Twitter(Network):
    
    auth = ''
    twitter_api =''
    
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET):
        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.OAUTH_TOKEN = OAUTH_TOKEN
        self.OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRET
    
    def login(self):
        self.auth = twitter.oauth.OAuth(self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET,
                           self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.twitter_api = twitter.Twitter(domain='api.twitter.com', 
                              api_version='1.1',
                              auth=self.auth
                             )
    def get_top(self):
        WORLD_WOE_ID = 1    
        
        world_trends = self.twitter_api.trends.place(_id=WORLD_WOE_ID)
        print world_trends
        
# CONSUMER_KEY = '6Zh1OZGtpQgTENiRDpY4zg'
# CONSUMER_SECRET = 'KIyMtMEuMMaU12HNEtM2G3x23Jge5yy1kxSKeeBPYvU'
# OAUTH_TOKEN = '75118840-YBAMIoZJPlYuGkdhsmutBdoagGRYKuv80eXtwlDgo'
# OAUTH_TOKEN_SECRET = 'cJuiGopAWmeoy01rgzN4XvlZhBsda4w5bl9P1ITHAtosx'
# tw = Twitter(CONSUMER_KEY,CONSUMER_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
# tw.login()
# tw.get_top()