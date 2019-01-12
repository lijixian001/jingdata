from config import HTMLTestRunner002
import unittest
from unittest import TestLoader,TestSuite,TestCase
from interface.homepage import MyTestCaseIndex,MYTestCaseNewinformation
from interface.news import NewsTest
from interface.idata import InsightDataTest
from interface.cytab import ProjectDetailsTest
from interface.insight import InsightTest
from interface.index import LibraryTest
from interface.workbench import WorkbenchTest
from email.header import Header
from  email.mime.text import MIMEText
import smtplib
import time
# H:\seleuim\jingdata_saas_py是GitHub
#
def allTest():
    suite1 = TestLoader().loadTestsFromTestCase(MyTestCaseIndex)
    suite2 = TestLoader().loadTestsFromTestCase(MYTestCaseNewinformation)
    suite3 = TestLoader().loadTestsFromTestCase(NewsTest)
    suite4 = TestLoader().loadTestsFromTestCase(InsightDataTest)
    suite5 = TestLoader().loadTestsFromTestCase(ProjectDetailsTest)  #全部公司表头字段筛选
    suite6 = TestLoader().loadTestsFromTestCase(InsightTest) # 全部公司表头字段排序
    suite7 = TestLoader().loadTestsFromTestCase(LibraryTest) # 指标库
    suite8 = TestLoader().loadTestsFromTestCase(WorkbenchTest) #工作台
    alltests = TestSuite([suite1,suite2,suite3,suite4,suite5,suite6,suite7,suite8])
    return alltests

if __name__ == '__main__':
    #now = time.strftime('%Y-%m-%d %H_%M_%S')
    filepath = './report/report.html'
    ftp = open(filepath, 'wb')
    runner = HTMLTestRunner002.HTMLTestRunner(stream=ftp, title='鲸准接口平台')
    runner.run(allTest())
    unittest.main()


