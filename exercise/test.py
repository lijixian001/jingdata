'''list = ['Google','Runoob',1997,2000]

print("原始列表：",list)
del  list[2]
print("删除第三个元素：",list)

list1,list2 = ['Google','Runoob','Taobao'],[456,700,999]
print("list1 最大元素值：",max(list1))
print("list2 最大元素值：",max(list2))

list=[]
for i in range(10):
    list.append(i)
print(list)


n = 100
sum = 0
counter = 1
while counter <= n:
    sum = sum + counter
    counter += 1
print("1到 %d 之和为：%d"%(n,sum))

var = 1
while var == 1:
    num = int(input("请输入一个数字："))
    print("你输入的数字是：",num)
print("Good bye!")

a = 0
while a < 5:
    print(a,"小于5")
    a = a + 1
else:
    print(a,"大于或等于5")

n = 100
sum = 0
counter = 1
while counter <= n:
    sum = sum + counter
    counter += 1
print("1到%d之和为：%d"%(n,sum))

a = 1
while (a):print('欢迎访问菜鸟教程')
print("GD")

a = ["baidu","Google","Runoob","Taobao","QQ"]
for i in range(len(a)):
    print(i,a[i])

list = [1,2,3,4]
it = iter(list)
for x in it:
    print(x,end="")


n1 = input('请输入用户名：')
n2 = input('请输入密码：')

n1 = "alex"
n2 = "root"

print(n1)
print(n2)

import time
i = 0
while i < 9:
    print('ok',time.time())
    i = i+1
1.输出：1 2 3 4 5 6 8 9 10
n = 1
while n < 11:
    if n == 7:
        pass
    else:
        print(n)
    n = n + 1
print('--end--')

#2.输出1-100以内的所有奇数
n = 1
while n < 101:
    temp = n % 2
    if temp == 0:
        print(n)
    else:
        pass
    n = n + 1
print('--end--')

#3.输出1-100以内的所有偶数
n = 1
while n < 101:
    temp = n % 2
    if temp == 0:
        print(n)
    else:
        pass
    n = n + 1
print('--end--')

#3.输出1-100的所有数的和
n = 1
s = 0
while n < 101:
    s = s + n
    n = n + 1
print(s)

L = [x * x for x in range(10)]
print(L)


def my_ads(x):
    if x >= 0:
        return x
    else:
        return -x
print(my_ads(-99))


inp = input('请输入会员级别')

if inp == "高级会员":
    print('美女')
elif inp == "白金会员":
    print('大模')
elif inp == "铂金会员":
    print('一线小明星')
else:
    print('城管')
print('请开始吧')

if 1==2:
    pass
else:
    print('1')

n = 1
while n < 11:
    if n == 7:
        pass
    else:
        print(n)
    n = n + 1

n = 1
while n < 101:
    temp = n % 2
    if temp == 0:
        pass
    else:
        print(n)
    n = n + 1

n = 1
while n < 101:
    temp = n % 2
    if temp == 0:
        print(n)
    else:
        pass
    n = n + 1

n = 1
num = 0
while n < 101:
    num = num + n
    n = n + 1
print(num)

n = 1
s = 0
while n < 100:
    temp = n % 2
    if temp == 0:
        s = s - n
    else:
        s = s + n
    n = n + 1
print(s)

#用户登录（三次重试机会）
c = 0
while c < 3:
    user = input('请输入用户名：')
    pwd = input('请输入密码密码:')
    if user == 'lijx' and pwd == '123':
        print('登录成功')
        break
    else:
        print('用户名或密码错误')
    c = c + 1

name = "郑建文"
v = "文" in name
print(v)

user = 'alex'
user.capitalize()
'''
import unittest
import HTMLTestRunner
import requests
import json
import pymysql
from config.url import url,headers
from unittest import TestLoader,TestSuite,TestCase
import hashlib

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

class MyTestCaseIndex(unittest.TestCase):

    def testindexdata(self):#首页
        a = loadDataBaseFromMyServer()[0]
        print(a)
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
        self.assertEqual(len(d['data']['banner']),2)
        self.assertEqual(code, 200)

    def testindexnewsletter(self):#快讯
        newsurl = url + "/api/indexinfo/index-newsletter"
        r = requests.get(newsurl)
        d = r.json()
        print("快讯数量： %s"%len(d['data']['list']))          #快讯数量
        self.assertEqual(len(d['data']['list']),6)

    def testinvestment(self):#最新融资事件
        investmenturl = url + "/api/indexinfo/index-investment-list"
        r = requests.get(investmenturl)
        d = r.json()
        print("最新融资事件数量： %s"%len(d['data']))          #最新融资事件数量  线上为6条
        self.assertEqual(len(d['data']),8)

    def testmonthmarket(self):#本月行情
        monthmarketurl = url + "/api/indexinfo/month-market"
        r = requests.get(monthmarketurl)
        d = r.json()
        print("本月行情种类：%s种"%len(d['data']))
        self.assertEqual(len(d['data']),6)

    def testtagdata(self):#热门领域-近一个月
        tagdataurl = url + "/api/indexinfo/tagdata"
        r = requests.get(tagdataurl)
        d = r.json()
        print("近一月热门领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

    def testtagdatahotdomainweek(self):#热门领域-近一周
        domainweekurl = url + "/api/indexinfo/tagdata?type=1&date_type=1"
        r = requests.get(domainweekurl)
        d = r.json()
        print("近一周热门领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']), 6)

    def testtagdatahotdomainmonth3(self):#热门领域-近三个月
        domainmonth3url = url + '/api/indexinfo/tagdata?type=1&date_type=3'
        r = requests.get(domainmonth3url)
        d = r.json()
        print("近三个月热门领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

    def testtagdatarisedomainweek(self):#上升领域-近一周
        risedomainweekurl = url + "/api/indexinfo/tagdata?type=2&date_type=1"
        r = requests.get(risedomainweekurl)
        d = r.json()
        print("近一周上升领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

    def testtagdatarisedomainmonth(self):#上升领域-近一个月
        risedomainmonthurl = url + "/api/indexinfo/tagdata?type=2&date_type=2"
        r = requests.get(risedomainmonthurl)
        d = r.json()
        print("近一个月上升领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

    def testtagdatarisedomainmonth3(self):#上升领域-近三个月
        risedomainmonth3url = url + "/api/indexinfo/tagdata?type=2&date_type=3"
        r = requests.get(risedomainmonth3url)
        d = r.json()
        print("近三个月上升领域数量：%s"%len(d['data']['list']))
        self.assertEqual(len(d['data']['list']),6)

    def testtopics(self):
        turl = url + "/api/promotion/list?curPage=1&pageSize=10"
        r = requests.get(turl,headers=headers)
        d = r.json()
        #print(len(d['data']))

class MYTestCaseNewinformation(unittest.TestCase):

    def testindexnewsletter(self):#快讯
        newsurl = url + "/api/indexinfo/index-newsletter"
        r = requests.get(newsurl)
        d = r.json()
        print("快讯数量： %s"%len(d['data']['list']))          #快讯数量
        self.assertEqual(len(d['data']['list']),6)

    def testinvestment(self):#最新融资事件
        investmenturl = url + "/api/indexinfo/index-investment-list"
        r = requests.get(investmenturl)
        d = r.json()
        print("最新融资事件数量： %s"%len(d['data']))          #最新融资事件数量  线上为6条
        self.assertEqual(len(d['data']),8)

def allTest():
    suite1 = TestLoader().loadTestsFromTestCase(MyTestCaseIndex)
    suite2 = TestLoader().loadTestsFromTestCase(MYTestCaseNewinformation)
    alltests = TestSuite([suite1,suite2])
    return alltests



if __name__ == '__main__':
    '''
    filepath = 'H:/htmlreport.html'
    ftp = open(filepath, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(TestMathFunc('testindexnewsletter'))
    suite.addTest(TestMathFunc('testinvestment'))
    suite.addTest(TestMathFunc('testtagdatahotdomainmonth3'))
    suite.addTest(TestMathFunc('testtagdatarisedomainweek'))
    suite.addTest(TestMathFunc('testtagdatarisedomainmonth'))
    suite.addTest(TestMathFunc('testtagdatarisedomainmonth3'))
    runner = HTMLTestRunner.HTMLTestRunner(stream=ftp, title='welcome to this web')
    runner.run(suite)
    unittest.main()
    '''

    #suite = unittest.TestSuite()
    #suite.addTest(TestMathFunc('testindexnewsletter'))
    #suite.addTest(TestMathFunc('testinvestment'))
    #suite.addTest(TestMathFunc('testtagdatahotdomainmonth3'))
    #suite.addTest(TestMathFunc('testtagdatarisedomainweek'))
    #suite.addTest(TestMathFunc('testtagdatarisedomainmonth'))
    #suite.addTest(TestMathFunc('testtagdatarisedomainmonth3'))
    filepath = 'H:/htmlreport.html'
    ftp = open(filepath, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=ftp, title='welcome to this web')
    runner.run(allTest())
    unittest.main()


