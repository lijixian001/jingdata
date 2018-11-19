import HTMLTestRunner
import json
import unittest
import requests
import time
from selenium import webdriver
from config.url import headers
from selenium.webdriver.support import expected_conditions as EC


class SetTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://insight-alpha.jingdata.com/api/v2/macro/349541/sub"
        #self.driver = webdriver.Chrome()
        #self.driver.get("http://www.cnblogs.com/yoyoketang")


    def testTitle(self):
        time.sleep(1)
        result = EC.title_is(u'上海-悠悠 - 博客园')(self.driver)
        print(result)
        self.assertTrue(result)

    def testAdd(self):
        result = 6-5
        hope = 1
        self.assertEqual(result,hope)
        print(result+hope)

    def testDivide(self):
        result = 7/2
        hope = 3.5
        self.assertEqual(result,hope)
        print(result)


    def testGetsub(self):
        r = requests.get(self.base_url,headers=headers)
        dicts = json.loads(r.text)
        print(dicts)
        print(headers)
        code = r.status_code
        self.assertEqual(code,200)

    def tearDown(self):
        self.driver.quit()



if __name__ == '_main_':
    unittest.main()
"""
    suite = unittest.TestSuite()
    suite.addTest(SetTest("test_getsub"))
    filepath = "H://Photo//1.html"
    fp=open(filepath, "wb")
    runner = HTMLTestRunner(stream=fp,title=u'XXXX接口测试用例',description=u'接口列表：')
    runner.run(suite)
    fp.close()
"""