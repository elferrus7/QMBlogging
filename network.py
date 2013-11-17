#Imports for Network class
import abc
import sys 

#Twitter specific imports
import twitter
import json
from twitter__login import login
from twitter__util import makeTwitterRequest
from twitter__util import getNextQueryMaxIdParam

from pymongo import MongoClient
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
    
    
    def login(self):
        return login()
    
    def get_trends(self):
        WORLD_WOE_ID = 1    
        
        world_trends = self.twitter_api.trends.place(_id=WORLD_WOE_ID)
        print json.dumps(world_trends, sort_keys=True,indent=1)
    
    def get_stream(self,TIMELINE_NAME,MAX_PAGES):
        USER = None
        
        KW = {  # For the Twitter API call
            'count': 200,
            'trim_user': 'true',
            'include_rts' : 'true',
            'since_id' : 1,
        }
        
        if TIMELINE_NAME == 'user':
            USER = sys.argv[3]
            KW['screen_name'] = USER
        if TIMELINE_NAME == 'home' and MAX_PAGES > 4:
            MAX_PAGES = 4
        if TIMELINE_NAME == 'user' and MAX_PAGES > 16:
            MAX_PAGES = 16
            
        t = self.login()
         
         
        client = MongoClient('localhost',27017)

        db = client.test_database
        posts = db.tw_data #Collection name
        posts.drop()
        
        api_call = getattr(t.statuses, TIMELINE_NAME + '_timeline')
        tweets = makeTwitterRequest(api_call, **KW)
        for tweet in tweets:
            if(tweet['lang']=='en'):
                print tweet['text']
                post_id = posts.insert(tweet)
                print '# post id'
                print post_id
        print 'Fetched %i tweets' % len(tweets)
        
        page_num = 1
        while page_num < MAX_PAGES and len(tweets) > 0:
        
            # Necessary for traversing the timeline in Twitter's v1.1 API.
            # See https://dev.twitter.com/docs/working-with-timelines
            KW['max_id'] = getNextQueryMaxIdParam(tweets)
        
            api_call = getattr(t.statuses, TIMELINE_NAME + '_timeline')
            tweets = makeTwitterRequest(api_call, **KW)
            #print json.dumps(tweets,indent = 3)
            for tweet in tweets:
                if(tweet['lang']=='en'):
                    print tweet['text']
                    post_id = posts.insert(tweet)
                    print '# post id'
                    print post_id
                
            print 'Fetched %i tweets' % len(tweets)
            page_num += 1
            

#tw = Twitter()
#tw.get_top()
#tw.get_stream('home', 16)