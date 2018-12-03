import unittest
import requests
import json
from config.url import url,headers
import pymysql
from config.sql import *
'''
config = {
    'host': "192.168.6.38",
    'user': "db-test",
    'password': "123456",
    'db': "jingdata_saas"
}
# 参数有个默认名字（请根据自己实际修改）
def loadDataBaseFromMyServer(database='jingdata_saas'):
    # 打开数据库连接
    db = pymysql.connect(**config)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    try:
        cursor.execute("select id from banner order by updated_at desc limit 0,1 " )
        # 使用 fetchall() 方法获取所有数据，获取结果是一个二维tuple
        data = cursor.fetchone()
    except BaseException as e:
        print(e)
        db.rollback()
    db.close()
    return data
'''

class MyTestCaseIndex(unittest.TestCase):

    def test_indexdata(self):#首页
        #a = bannerid()[0]
        #print(a)
        iurl = url + "/api/indexinfo/indexdata"
        r = requests.get(iurl)
        d = json.loads(r.text)
        code = r.status_code
        print(len(d['data']))
        #print(d['data']['research'])
        #print(d['data']['research'][0])
        print("研究报告数: %s"%len(d['data']['research']))     #研究报告篇幅
        print("洞见专题数：%s"%len(d['data']['promotion']))    #洞见专题数量
        print("热门项目数：%s"%len(d['data']['hot_company']))  #热门项目数量
        print("热门投资机构：%s"%len(d['data']['hot_organization']))#热门投资机构数
        print("Banner数：%s"%len(d['data']['banner']))         #banner数量
        self.assertEqual(len(d['data']['research']),7)
        self.assertEqual(len(d['data']['promotion']),4)
        self.assertEqual(len(d['data']['hot_company']),7)     #页面显示为6条数据
        self.assertEqual(len(d['data']['hot_organization']),7)#页面显示为6条数据
        #self.assertEqual(len(d['data']['banner']),2)
        self.assertEqual(code, 200)

    def test_indexnewsletter(self):#快讯
        newsurl = url + "/api/indexinfo/index-newsletter"
        r = requests.get(newsurl)
        d = r.json()
        print("快讯数量： %s"%len(d['data']['list']))          #快讯数量
        self.assertEqual(len(d['data']['list']),6)

    def test_investment(self):#最新融资事件
        investmenturl = url + "/api/indexinfo/index-investment-list"
        r = requests.get(investmenturl)
        d = r.json()
        print("最新融资事件数量： %s"%len(d['data']))          #最新融资事件数量  线上为6条
        self.assertEqual(len(d['data']),8)

    def test_monthmarket(self):#本月行情
        monthmarketurl = url + "/api/indexinfo/month-market"
        r = requests.get(monthmarketurl)
        d = r.json()
        print("本月行情种类：%s种"%len(d['data']))
        self.assertEqual(len(d['data']),6)

    def test_tagdata(self):#热门领域-近一个月
        tagdataurl = url + "/api/indexinfo/tagdata"
        r = requests.get(tagdataurl)
        d = r.json()
        print("近一月热门领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

    def test_tagdatahotdomainweek(self):#热门领域-近一周
        domainweekurl = url + "/api/indexinfo/tagdata?type=1&date_type=1"
        r = requests.get(domainweekurl)
        d = r.json()
        print("近一周热门领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']), 6)

    def test_tagdatahotdomainmonth3(self):#热门领域-近三个月
        domainmonth3url = url + '/api/indexinfo/tagdata?type=1&date_type=3'
        r = requests.get(domainmonth3url)
        d = r.json()
        print("近三个月热门领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

    def test_tagdatarisedomainweek(self):#上升领域-近一周
        risedomainweekurl = url + "/api/indexinfo/tagdata?type=2&date_type=1"
        r = requests.get(risedomainweekurl)
        d = r.json()
        print("近一周上升领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

    def test_tagdatarisedomainmonth(self):#上升领域-近一个月
        risedomainmonthurl = url + "/api/indexinfo/tagdata?type=2&date_type=2"
        r = requests.get(risedomainmonthurl)
        d = r.json()
        print("近一个月上升领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

    def test_tagdatarisedomainmonth3(self):#上升领域-近三个月
        risedomainmonth3url = url + "/api/indexinfo/tagdata?type=2&date_type=3"
        r = requests.get(risedomainmonth3url)
        d = r.json()
        print("近三个月上升领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

class MYTestCaseNewinformation(unittest.TestCase):

    def test_indexnewsletter(self):#快讯
        newsurl = url + "/api/indexinfo/index-newsletter"
        r = requests.get(newsurl)
        d = r.json()
        print("快讯数量： %s"%len(d['data']['list']))          #快讯数量
        self.assertEqual(len(d['data']['list']),6)

    def test_investment(self):#最新融资事件
        investmenturl = url + "/api/indexinfo/index-investment-list"
        r = requests.get(investmenturl)
        d = r.json()
        print("最新融资事件数量： %s"%len(d['data']))          #最新融资事件数量  线上为6条
        self.assertEqual(len(d['data']),8)

if __name__ == '__main__':
    unittest.main()


'''
if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(MyTestCaseIndex("testindexdata"))
    #suite.addTest(unittest.TestSuite(MYTestCaseNewinformation))
    file_path = "H:\\a.html"
    file_result = open(file_path, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream = file_result, title = u'参数化测试数据', description = u'描述'
    )
    runner.run(suite)
    file_result.close()
'''