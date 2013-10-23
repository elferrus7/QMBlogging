import httplib, urllib
# Please check first our User's Reference Manual. "http://www.bitext.com/btxt_docs/Bitext_API-Reference-Manual_EN.pdf"

# Set-up the values of the form fields for the POST message
#
# !!!! Fill up with your actual Username and Password !!!!!
usr = 'elferrus7'
pwd = 'mmohuevos7'

# You should normally would like to make a loop for setting values for these two fields...
txt = 'The API is very good'
id = '0001'

# English language is assumed. 
#    Otherwise replace ENG by ESP, POR, ITA, FRA*, DEU*, CAT* as appropriate.
#    You can also set dynamically the value for the language field if you have text for multiple languages
#    The service per each language expects text in the referred languge. There is no automatic language identification in the Evaluation API.
#    *Please note that not all services (see below) are currently available for these "*"-marked languages.
lang='ENG'

# Sentiment Analysis service is assumed. 
#    Otherwise replace "Val" by "Conc" (= concept extraction), "Ent" (=entity extraction) or "Cat" (=text categorization)
#    Services other than "Val" might require slightly differente parameters to be "POST"ed. Please check the User's Reference Manual.
#    For other possible values for certain parameters, please check the User's Reference Manual.
service='/WS_Nops_Val/Service.aspx'

# Service params
params = urllib.urlencode({'User': '%s' % usr, 'Pass': '%s' %pwd, 'Lang': '%s' % lang, 'ID': '%s' %id, 'Text': '%s' % txt, 'Detail': 'Detailed', 'OutFormat':'JSON', 'Normalized': 'No', 'Theme': 'Gen'})

# HTML headers required
headers = {"Content-type": "application/x-www-form-urlencoded"}

# Server. In case of need, please check with Bitext for an updatged list of available servers
server="svc8.bitext.com"

# The POST
conn = httplib.HTTPConnection("%s" % server)
conn.request("POST", "%s" % service, params, headers)
response = conn.getresponse()
data = response.read()
conn.close()

print data

# Do something with "data"...