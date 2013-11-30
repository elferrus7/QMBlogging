import network
#import analysis #No longer in use
import report
#import subprocess
import urllib

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
#tw.get_stream('home', 16)
#tw.get_search('#pokemon')



print '############################################'
print '#         Semantic Analysis                #'
print '############################################'

#url = 'http://localhost/freeling/freeling_ana.php'
#response = urllib.urlopen(url).read() 
#print response


print '############################################'
print '#        Report and Extra Analysis         #'
print '############################################'

r = report.Report()
r.graph_entities()