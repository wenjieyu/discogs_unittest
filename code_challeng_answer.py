import requests
import unittest
from jsonpath_ng import jsonpath, parse

class TestDiscogs(unittest.TestCase):
    # valid key
    key = "sEfcNKVvbrdRSENJaWSy"
    # invalid key
    key_invalid = "EfcNKVvbrdRSENJaWSy"

    secret = "vlyhhCzDfReNaOaNSBzRwCoTAVRPxODt"
    discog_url = "https://api.discogs.com/database"

    defaut_per_page = 50
    specific_limit_per_page = 20
    max_per_page = 100
    over_max_per_page = 110
      

    @classmethod
    def setUpClass(self):
        auth = "Discogs key={}, secret={}".format(self.key, self.secret)
        auth_invalid = "Discogs key={}, secret={}".format(self.key_invalid, self.secret)
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth
            }

        self.headers_invalid = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth_invalid
            }
    
        #If a specific limit is specified, the api must return the requested number of record per pages.  
        self.pagni_param_specific_limit ={
            "per_page": self.specific_limit_per_page

            }
       #The api will return a maximun number of result per pages, even if we provide a large limit value.     
        self.pagni_param_over_max ={
            "per_page": self.over_max_per_page
            }

    def test_basic_response(self):
        res = requests.get("{}/search".format(self.discog_url),headers=self.headers)
 
        print(res.request)
        print(res.json())
    
        if res.status_code==200:
            access = True
        else:
            access = False    
        res = res.json()
        jsonpath_expression = parse("$.pagination.per_page")

        for match in jsonpath_expression.find(res):
	         per_page_num = match.value
        
        #asserting access success
        self.assertTrue(access)

        #asserting default per page without limit specified
        self.assertEqual(per_page_num,self.defaut_per_page)

       

    def test_basic_response_fail(self):
        res = requests.get("{}/search".format(self.discog_url),headers=self.headers_invalid)
 
        print(res.request)
        print(res.json())
    
        if res.status_code==401:
            access = True
        else:
            access = False    
        #asserting access no success

        self.assertTrue(access)   

    def test_pagni_response_limit_specific(self):
        res = requests.get("{}/search".format(self.discog_url), params =self.pagni_param_specific_limit, headers=self.headers)
 
        print(res.request)
        print(res.json())
        res = res.json()
        jsonpath_expression = parse("$.pagination.per_page")

        for match in jsonpath_expression.find(res):
	         per_page_num = match.value
        
        #asserting per page with specific limit

        self.assertEqual(per_page_num,self.specific_limit_per_page)
    

    def test_pagni_response_over_max(self):
        res = requests.get("{}/search".format(self.discog_url), params =self.pagni_param_over_max, headers=self.headers)
 
        print(res.request)
        print(res.json())
        res = res.json()
        jsonpath_expression = parse("$.pagination.per_page")

        for match in jsonpath_expression.find(res):
	         per_page_num = match.value
        #asserting max per_page with limit over max specified     
        self.assertEqual(per_page_num,self.max_per_page)

if __name__ == '__main__':
    #unittest.main()
    unittest.main(verbosity=2)
