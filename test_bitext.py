'''
Created on Oct 9, 2013

@author: elferrus7
'''
import requests

postData = {'User':'elferrus7',
            'Pass':'mmohuevos7',
            'Lang':'English', 
            'ID':'123', 
            'Text':'I really enjoyed using the Canon Ixus in Madrid',
            'OutFormat':'JSON',
            'Normalized':'No',
            'Theme':'Client'}
r = requests.post('http://svc9.bitext.com/WS_NOps_Ent/Service.aspx',params=postData)

print r.url