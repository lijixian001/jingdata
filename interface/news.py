
import unittest
import requests
import json
from config.url import url,headers
import pymysql

config = {
    'host': "192.168.6.38",
    'user': "db-test",
    'password': "123456",
    'db': "jingdata_saas"
}

def loadDataBaseFromMyServer(database='jingdata_saas'):# 专题id
    # 打开数据库连接
    db = pymysql.connect(**config)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    try:
        cursor.execute("select count(*) from promotion where public_status = 1 or public_status = 0 " )#专题id
        # 使用 fetchall() 方法获取所有数据，获取结果是一个二维tuple
        data = cursor.fetchone()
    except BaseException as e:
        print(e)
        db.rollback()
    db.close()
    return data

def topicDetailsid(database='jingdata_saas'):#专题数量  r = requests.post(headersort_url, data, headers=headers)
    # 打开数据库连接
    db = pymysql.connect(**config)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:
        cursor.execute("select id from promotion where public_status = 1 or public_status = 0 " )
        # 使用 fetchall() 方法获取所有数据，获取结果是一个二维tuple
        data = cursor.fetchone()
    except BaseException as e:
        print(e)
        db.rollback()
    db.close()
    return data

class NewsTest(unittest.TestCase):

    def test_newsletter(self):#7✖24H快讯
        newsletterurl = url + "/api/news-letter/list?pageSize=10&id="
        r = requests.get(newsletterurl,headers = headers)
        d = r.json()
        print("7*24H快讯数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),0)

    def test_promotion(self):#洞见专题
        #b = loadDataBaseFromMyServer()[0]
        #print(b)
        promotionurl = url + "/api/promotion/list?curPage=1&pageSize=10"
        r = requests.get(promotionurl,headers = headers)
        d = r.json()
        c = d['data']['list'][0]['id']#获取第一个专题id
        print(c)
        print("洞见专题数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),8)

    def test_topicDetail(self):#专题详情页
        #tdid = topicDetailsid()[0]
        #topicDetailurl = url + "/api/promotion/" + str(tdid)
        topicDetailurl = url + "/api/promotion/" + str(7)
        r = requests.get(topicDetailurl,headers = headers)
        d = r.json()
        print(topicDetailurl)
        print("该洞见专题id = %s"%(d['data']['id']))
        self.assertEqual(d['data']['id'],7)

    def test_departmenttype(self):#政策法规分类
        departmenturl = url + "/api/news-research/lawsdict"
        r = requests.get(departmenturl,headers = headers)
        d = r.json()
        print("政策法规分类数量 : %s"%len(d['data']))
        self.assertEqual(len(d['data']),17)

    def test_department(self):#政策法规
        departmenturl = url + "/api/news-research/lawslist?department=&keyword=&pageSize=10&curPage=1"
        r = requests.get(departmenturl,headers = headers)
        d = r.json()
        print("默认展示政策法规数量 : %s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),10)

    def test_departmentresearch(self):#政策法规搜索
        #departmenturl = url + "/api/news-research/lawslist?department=&keyword=政策法规&pageSize=10&curPage=1"
        departmenturl = url + "/api/news-research/lawslist?department=&keyword=政策法规"
        r = requests.get(departmenturl,headers = headers)
        d = r.json()
        print("默认展示匹配结果数 = %s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),20)

    def test_newslist(self):#全部新闻
        newslisturl = url + "/api/news/list"
        r = requests.post(newslisturl,headers = headers)
        d = r.json()
        print('全部新闻数量 ： %s'%(d['data']['total']))
        self.assertGreaterEqual(d['data']['total'],203272)

    def test_industrydict(self):#新闻情报行业字典
        industrydicturl = url + "/api/redis/dictcache?type=2&key=crm-dict_industry"
        r = requests.get(industrydicturl,headers = headers)
        d = r.json()
        print("全部新闻所属行业字典数量 ： %s"%len(d['data']))
        self.assertEqual(len(d['data']),28)

    def test_reporttype(self):#全部新闻报道类型
        reportypeurl = url + "/api/news/report-type"
        r = requests.get(reportypeurl,headers = headers)
        d = r.json()
        print("新闻情报全部分类为： %s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),8)

    def test_newstimeseach(self):#全部新闻跟据时间进行筛选
        newstimeurl = url + "/api/news/list"
        test_data = {'ServiceCode': 'aaaa', 'b': 'bbbbb'}
        data = {
                'curPage': 1,
                'industry': "",
                'keyword': "",
                'pageSize': 10,
                'reportTime': "2018-11-01_2018-11-13",
                'reportType': []
                }
        r = requests.post(newstimeurl,data,headers = headers)
        d = r.json()
        print('处于2018-11-01_2018-11-13时间段的新闻数 ： %s'%(d['data']['total'] ))
        self.assertGreaterEqual(d['data']['total'],4338)

    def test_newest(self):#最新获投
        newesturl =  url + "/api/news/list"
        data = {"reportTime": "", "industry": "", "reportType": [1], "keyword": "", "pageSize": 10, "curPage": 1}
        r = requests.post(newesturl,data,headers = headers)
        d = r.json()
        print("最新获投新闻数 ： %s"%(d['data']['total']))
        self.assertGreaterEqual(d['data']['total'], 37805)

    def test_newIPO(self):#IPO/并购
        newesturl =  url + "/api/news/list"
        data = {"reportTime": "", "industry": "", "reportType": [2], "keyword": "", "pageSize": 10, "curPage": 1}
        r = requests.post(newesturl, data, headers=headers)
        d = r.json()
        print("IPO/并购新闻数 ： %s" % (d['data']['total']))
        self.assertGreaterEqual(d['data']['total'],5541)

    def test_financing(self):#资本动态
        financingurl =  url + "/api/news/list"
        data = {"reportTime": "", "industry": "", "reportType": [3], "keyword": "", "pageSize": 10, "curPage": 1}
        r = requests.post(financingurl, data, headers=headers)
        d = r.json()
        print("资本动态新闻数 ： %s" % (d['data']['total']))
        self.assertGreaterEqual(d['data']['total'], 5024)

    def test_unicorn(self):#独角兽
        unicornurl =  url + "/api/news/list"
        data = {"reportTime": "", "industry": "", "reportType": [4], "keyword": "", "pageSize": 10, "curPage": 1}
        r = requests.post(unicornurl, data, headers=headers)
        d = r.json()
        print("独角兽新闻数 ： %s" % (d['data']['total']))
        self.assertGreaterEqual(d['data']['total'], 12557)

    def test_company_dynamic(self):#公司动态
        company_dynamicurl =  url + "/api/news/list"
        data = {"reportTime": "", "industry": "", "reportType": [5], "keyword": "", "pageSize": 10, "curPage": 1}
        r = requests.post(company_dynamicurl, data, headers=headers)
        d = r.json()
        #print(d)
        print("公司动态新闻数 ： %s" %(d['data']['total']))
        self.assertGreaterEqual(d['data']['total'], 84475)

    def test_company_research(self):#公司研究
        company_research_url =  url + "/api/news/list"
        data = {"reportTime": "", "industry": "", "reportType": [6], "keyword": "", "pageSize": 10, "curPage": 1}
        r = requests.post(company_research_url, data, headers=headers)
        d = r.json()
        print("公司研究新闻数 ： %s" % (d['data']['total']))
        self.assertGreaterEqual(d['data']['total'], 16570)

    def test_people_view(self):#人物观点
        people_view_url =  url + "/api/news/list"
        data = {"reportTime": "", "industry": "", "reportType": [7], "keyword": "", "pageSize": 10, "curPage": 1}
        r = requests.post(people_view_url, data, headers=headers)
        d = r.json()
        print("人物观点新闻数 ： %s" % (d['data']['total']))
        self.assertGreaterEqual(d['data']['total'], 12241)

    def test_people_view001(self):#全部新闻报道类型为—其他
        people_view_url =  url + "/api/news/list"
        data = {"reportTime":"","industry":"","reportType":[0],"keyword":"","pageSize":10,"curPage":1}
        #x = json.dumps(data)
        r = requests.post(people_view_url, json = data, headers = headers)
        d = r.json()
        print("报道类型为—其他的新闻数 ： %s" % (d['data']['total']))
        self.assertGreaterEqual(d['data']['total'], 12241)

if __name__ == '__main__':
    unittest.main