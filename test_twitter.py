'''
Created on Oct 9, 2013

@author: elferrus7
'''
import twitter

CONSUMER_KEY = '6Zh1OZGtpQgTENiRDpY4zg'
CONSUMER_SECRET = 'KIyMtMEuMMaU12HNEtM2G3x23Jge5yy1kxSKeeBPYvU'
OAUTH_TOKEN = '75118840-YBAMIoZJPlYuGkdhsmutBdoagGRYKuv80eXtwlDgo'
OAUTH_TOKEN_SECRET = 'cJuiGopAWmeoy01rgzN4XvlZhBsda4w5bl9P1ITHAtosx'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(domain='api.twitter.com', 
                              api_version='1.1',
                              auth=auth
                             )

WORLD_WOE_ID = 1 

# Prefix id with the underscore for query string parameterization.
# Without the underscore, it's appended to the URL itself
world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
print world_trends

# Like all other APIs, search requests now require authentication and have a slightly different request and
# response format. See https://dev.twitter.com/docs/api/1.1/get/search/tweets

q = "SNL"
count = 100

search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']

# v1.1 of Twitter's API provides a value in the response for the next batch of results that needs to be parsed out
# and passed back in as keyword args if you want to retrieve more than one page. It appears in the 'search_metadata'
# field of the response object and has the following form:'?max_id=313519052523986943&q=NCAA&include_entities=1'
# The tweets themselves are encoded in the 'statuses' field of the response


# Here's how you would grab five more batches of results and collect the statuses as a list
for _ in range(5): 
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e: # No more results when next_results doesn't exist
        break

    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ]) # Create a dictionary from the query string params
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']
    
    import json
    #print json.dumps(statuses[0:2], indent=1)
    #print json.dumps(search_results) # Only print a couple of tweets here in IPython Notebook
    
    #A simple list comprehension in Python
    
    tweets = [ status['text'] for status in statuses ]

    #print tweets[0]
    
    #Calculating lexical diversity for tweets
    
    words = []
    for t in tweets:
        words += [ w for w in t.split() ]
    
    # total words
    #print len(words) 
    
    # unique words
    #print len(set(words)) 
    
    # lexical diversity
    #print 1.0*len(set(words))/len(words) 
    
    # avg words per tweet
    #print 1.0*sum([ len(t.split()) for t in tweets ])/len(tweets) 
    
    ##Using NLTK to perform basic frequency analysis
    #import nltk

    #freq_dist = nltk.FreqDist(words)
    #print freq_dist.keys()[:50] # 50 most frequent tokens
    #print freq_dist.keys()[-50:] # 50 least frequent tokens
    
    #effectively do the same thing.
    from collections import Counter

    counter = Counter(words)
    #print counter.most_common(50)
    #print counter.most_common()[-50:] # doesn't have a least_common method, so get them all and slice
    
    #Using regular expressions to find retweets
    
    import re
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    example_tweets = ["RT @SocialWebMining Justin Bieber is on SNL 2nite. w00t?!?", 
                      "Justin Bieber is on SNL 2nite. w00t?!? (via @SocialWebMining)"]
    #for t in example_tweets:
    #    print rt_patterns.findall(t)
    
    # Building and analyzing a graph describing who retweeted whom
    import networkx as nx
    
    g = nx.DiGraph()
    
    def get_rt_sources(tweet):
        rt_patterns = re.compile(r'(RT|via)((?:\b\W*@\w+)+)', re.IGNORECASE)
        return [ source.strip()
                 for tuple in rt_patterns.findall(tweet)
                     for source in tuple
                         if source not in ("RT", "via") ]
    
    for status in statuses:
        rt_sources = get_rt_sources(status['text'])
        if not rt_sources: continue
        for rt_source in rt_sources:
            g.add_edge(rt_source, status['user']['screen_name'], {'tweet_id' : status['id']})
                
    #print nx.info(g)
    #print g.edges(data=True)[0]
    #print len(nx.connected_components(g.to_undirected()))
    #print sorted(nx.degree(g).values())