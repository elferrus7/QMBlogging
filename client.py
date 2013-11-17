import network
import analysis
import report
from pymongo import MongoClient

print ''
print '############################################'
print '#         QMBloggin Prototipe              #'
print '############################################'
print ''
print '############################################'
print '#         Data Mining with twitter         #'
print '############################################'

tw = network.Twitter()
tw.get_stream('home', 16)



print '############################################'
print '#         Semantic Analysis                #'
print '############################################'

alchemy = analysis.Alchemy()

client = MongoClient('localhost',27017)
db = client.test_database
posts = db.tw_data #Collection name
for tweet in posts.find():
    alchemy.get_entities(txt=tweet['text'])

print '############################################'
print '#        Report and Extra Analysis         #'
print '############################################'

r = report.Report()
r.graph_entities()