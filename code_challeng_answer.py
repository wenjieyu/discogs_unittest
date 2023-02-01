import requests
import unittest
from jsonpath_ng import jsonpath, parse

class TestDiscogs(unittest.TestCase):
    # valid key
    key = "sEfcNKVvbrdRSENJaWSy"
    # invalid key
    #key = "EfcNKVvbrdRSENJaWSy"
    
    secret = "vlyhhCzDfReNaOaNSBzRwCoTAVRPxODt"
    discog_url = "https://api.discogs.com/database"
    
    @classmethod
    def setUpClass(self):
        auth = "Discogs key={}, secret={}".format(self.key, self.secret)
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth
            }
    # check Access success or not 
    def test_basic_response(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)
 
        print(res.request)
        print(res.json())
        jsondata = res.json()

        #check if there is "message" key in the res.json() if yes then access failed otherwise access succeed 
        if"message" in jsondata:
            access = False
        else:  
            access = True
        
        #asserting
        self.assertTrue(access)

    # If no limit specified, we return default number of record per page
    
    def test_default_Pagination(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)
 
        print(res.request)
        print(res.json())
        jsondata = res.json()

        jsonpath_expression = parse("$.pagination.per_page")

        for match in jsonpath_expression.find(jsondata):
	         per_page_num = match.value
        
        #asserting
        self.assertEqual(per_page_num,50)
        

if __name__ == '__main__':
    #unittest.main()
    unittest.main(verbosity=2)