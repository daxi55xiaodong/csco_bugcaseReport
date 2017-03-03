'''
http://requests-oauthlib.readthedocs.io/en/latest/oauth1_workflow.html
https://search-prd.cisco.com/topic/news/cisco/eng/cdets-trolls/dsc07889.html
'''

import requests, os
from requests_oauthlib import OAuth1Session

#import xml.dom.minidom

class QueryTask(object):
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret
    def make_request(self,request_url):
        cdets = OAuth1Session(self.key,self.secret)
        url = request_url
        response = cdets.get(url)
        
        '''test print'''
        #print response.content
        '''test print'''
        try:
            f = file('./xmlFile/WSAPI_buffer.xml','w+')
            f.write(response.content)
            f.close()
        except:
            print '>>>>!error! write WSAPI_buffer.xml error!'
        
        

if __name__ == '__main__':
    CallWSAPI = QueryTask("de7f6cf0-f70a-4eb5-93df-0466ac4fba35","4vHiua085XxnERv58lXctmtqZKXIIRWT")
    URL = 'https://cdetsng.cisco.com/wsapi/latest/api//search?syntax=cdets&criteria=%28%5BProduct%5D%3D%27pss-sntc%27%29&fields=Identifier%2CSeverity-desc%2CStatus-desc%2CHeadline%2CSummary%2CProject%2CProduct%2CComponent%2CCust%20Priority%2CDE-priority-desc%2CDE-manager%2CSubmitter-id%2CSubmitted-on%2COriginal-found-during%2CFound-during%2CFound%2COriginal-found%2CTAC-SR-count%2CCF-origin%2CTrouble-tickets%2CCustomer-name%2CStatus%2CTickets-count&start=0&count=0'

    CallWSAPI.make_request(URL)

