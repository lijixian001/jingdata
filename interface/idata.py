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

class InsightDataTest(unittest.TestCase):

    #洞见数据menu
    def test_idata_menu(self):
        menu_url = url + '/api/insight/menu'
        r = requests.get(menu_url,headers = headers)
        d = r.json()
        x = len(d['data'][0]['children'])
        print('【洞见数据左侧菜单栏第一个Menu有',x,'不同类型的公司列表】')
        self.assertEqual(x,6)

    #全部公司列表
    def test_all_company(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
                }
        r = requests.post(all_company_url,data,headers = headers)
        d = r.json()
        print("【全部公司数量为 ： %s"%(d['data']['total']),'家】')
        self.assertEqual(len(d['data']['data']),20)

    #全部公司列表表头字段
    def test_all_company_allFieldsCompany(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
            }
        r = requests.post(all_company_url, data, headers=headers)
        d = r.json()
        print('【全部公司列表全部表头字段为： %s' % len(d['data']['allFieldsCompany']),'】')
        self.assertEqual(len(d['data']['allFieldsCompany']), 30)

    #全部公司可筛选表头字段
    def test_all_company_selectFieldsCompany(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
            }
        r = requests.post(all_company_url, data, headers=headers)
        d = r.json()
        print('【全部公司可筛选表头字段为： %s' % len(d['data']['selectFieldsCompany']),'】')
        self.assertEqual(len(d['data']['selectFieldsCompany']), 18)

    #全部公司默认展示表头字段
    def test_all_company_showFieldsCompany(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
                }
        r = requests.post(all_company_url,data,headers = headers)
        d = r.json()
        print('【全部公司列表默认展示表头字段为 ： %s'%(len(d['data']['showFieldsCompany'])),'】')
        self.assertEqual(len(d['data']['showFieldsCompany']),12)

    #全部公司列表可筛选字段字典
    def test_all_company_selectFieldsdict(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
                }
        r = requests.post(all_company_url,data,headers = headers)
        d = r.json()
        print('【全部公司可筛选字段字典【行业】数量为： %s' % len(d['data']['charts']['finance_phase']['buckets']),'】')
        print('【全部公司可筛选字段字典【所在地】数量为： %s'%len(d['data']['charts']['address1']['buckets']),'】')
        print('【全部公司可筛选字段字典【最近融资轮次】数量为： %s' % len(d['data']['charts']['address1']['buckets']),'】')
        self.assertEqual(len(d['data']['charts']['industry']['buckets']),28)
        self.assertEqual(len(d['data']['charts']['address1']['buckets']),60)
        self.assertEqual(len(d['data']['charts']['finance_phase']['buckets']),20)

    #全部公司列表检索示例
    def test_search_example(self):
        search_example_url = url + "/api/upgradefilter/getprefabricatedcondition?type=100"
        r = requests.get(search_example_url,headers = headers)
        d = r.json()
        print('【检索示例名称 ： %s'%(d['data'][0]['name']),(d['data'][1]['name']),'】')
        self.assertEqual(d['data'][0]['name'],'腾讯投资的全部项目')
        self.assertEqual(d['data'][1]['name'],'阿里巴巴并购的项目')

    #高级检索-所在地-字典
    def test_all_company_address_dict(self):
        address_dict_url = url + '/api/search/tagaddress?type=2&name=0'
        r = requests.get(address_dict_url, headers=headers)
        d = r.json()
        print('【高级检索-所在地一级行政区数量为： %s' % len(d['data']), '个】')
        self.assertEqual(len(d['data']), 35)

    #高级检索-最近融资轮次字典
    def test_all_company_phase_dict(self):
        phase_dict_url = url + "/api/redis/dictcache?type=2&key=crm-dict_phase"
        r = requests.get(phase_dict_url,headers = headers)
        d = r.json()
        print('【高级检索-最近融资轮次字典数量 : %s'%len(d['data']),'】')
        self.assertEqual(len(d['data']),22)

    #高级检索-行业字典数量
    def test_all_company_industry_dict(self):
        industry_idct_url = url + "/api/redis/dictcache?type=2&key=crm-dict_industry"
        r = requests.get(industry_idct_url,headers = headers)
        d = r.json()
        print('【高级检索-行业字典数量 ： %s'%len(d['data']),'】')
        self.assertEqual(len(d['data']),28)

    #高级检索-标签
    def test_all_company_tagstree(self):
        tagstree_url = url + '/api/search/gettagstree'
        r = requests.get(tagstree_url,headers = headers)
        d = r.json()
        print('【高级检索-标签树数量为： %s'%len(d['data']),'】')
        self.assertEqual(len(d['data']),28)

    #高级检索-报道媒体
    def test_all_company_getdefaulttagwebsite(self):
        getdefaulttagwebsite_url = url + '/api/search/getdefaulttagwebsite?type=0'
        r = requests.get(getdefaulttagwebsite_url,headers =headers)
        d = r.json()
        print('【高级检索-报道媒体数量为： %s'%len(d['data']),'家】')
        #print('第一序列报道媒体为： %s'%d['data'][0])
        #self.assertEqual(len(d['data']),6)
        self.assertEqual(d['data'][0],'36氪')

    #高级检索-第一个下拉框选项
    def test_all_company_dictbyobject(self):
        dictbyobject_url = url + '/api/upgradefilter/dictbyobject?object=company&parent_id=458'
        r = requests.get(dictbyobject_url,headers = headers)
        d = r.json()
        print('【高级检索-第一个下拉框内选项有 ： %s'%len(d['data']),'个】')
        self.assertEqual(len(d['data']),3)

    #全部公司表头字段筛选
    def test_all_company_select_name(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"name.or\":[\"阿里巴巴\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【公司简称输入阿里巴巴关键词筛选结果为： %s'%(d['data']['total']),'家】')
        self.assertEqual(len(d['data']['data']),20)

    #高级检索-表头字段筛选-公司简称-下拉选项
    def test_name_select_pull(self):
        name_select_url = url + '/api/upgradefilter/getreleatenamebykey?object=company&name=阿里巴巴'
        r = requests.get(name_select_url,headers = headers)
        d = r.json()
        print('【公司简称字段筛选下拉选项数量： %s'%len(d['data']),'】')
        self.assertEqual(len(d['data']),10)

    #高级检索-表头字段筛选-最近融资轮次
    def test_phase_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.latest_phase.or\":[30,40]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【最近融资轮次输入A轮、B轮筛选结果为： %s'%(d['data']['total']),'条】')
        self.assertEqual(len(d['data']['data']),20)

    #高级检索-表头字段筛选-最近融资时间
    def test_time_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.latest_finance_date\":[\"2018-10-01\",\"2018-10-31\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【最近融资时间为10月份的筛选结果为： %s'%(d['data']['total']),'条】')
        self.assertEqual(len(d['data']['data']),20)

    #高级检索-表头字段筛选-行业
    def test_industry_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"industry.or\":[1]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【行业是电商的筛选结果为： %s'%(d['data']['total']),'条】')
        self.assertEqual(len(d['data']['data']),20)

    # 高级检索-表头字段筛选-所在地
    def test_industry_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"address.or\":[101]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【所在地是北京的筛选结果为： %s'%(d['data']['total']),'条】')
        self.assertEqual(len(d['data']['data']),20)

    # 高级检索-表头字段筛选-一句话简介
    def test_description_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"address.or\":[],\"brief.or\":[\"电商\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【一句话简介包含电商的筛选结果为： %s'%(d['data']['total']),'条】')
        self.assertEqual(len(d['data']['data']),20)

    # 高级检索-表头字段筛选-最近一轮融资额
    def test_finance_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"brief.or\":[\"电商\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【最近一轮融资额等于1000W人民币的筛选结果为： %s'%(d['data']['total']),'条】')
        self.assertEqual(len(d['data']['data']),20)

    # 高级检索-表头字段筛选-历史总融资额
    def test_historyfinance_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.total_finance_amount\":[3300,3300]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【历史总融资额等于500W美元的筛选结果为： %s'%(d['data']['total']),'条】')
        self.assertEqual(len(d['data']['data']),20)

    # 高级检索-表头字段筛选-估值
    def test_valuation_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.latest_valuation\":[\"1000\",\"\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【估值大于1000W人民币的筛选结果为： %s'%(d['data']['total']),'条】')
        self.assertEqual(len(d['data']['data']),20)

    def test_starttime_select(self):
        #高级检索-表头字段筛选-创办时间
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.latest_valuation\":[null,\"\"],\"start_date\":[\"2017-01-01\",\"2017-12-31\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('【创办时间是去年的筛选结果为： %s'%(d['data']['total']),'条】')
        self.assertEqual(len(d['data']['data']),20)

    # 全部公司-表头字段-排序-热度-降序DESC
    def test_hot_score_desc(self): #表头字段排序-热度-降序Desc
        headersort_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_score\",\"param\":[\"desc\"]}]}"}
        r = requests.post(headersort_url,data,headers = headers)
        d = r.json()
        print('【全部公司列表热度最高公司名称、及热度值为： %s'%(d['data']['data'][0]['name']),'、%s'%(d['data']['data'][0]['stat_rank.hot_score']),'】')
        self.assertGreaterEqual(d['data']['data'][0]['stat_rank.hot_score'],d['data']['data'][1]['stat_rank.hot_score'])

    # 全部公司-表头字段-排序-热度-升序ASC
    def test_hot_score_asc(self):
        headersort_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_score\",\"param\":[\"asc\"]}]}"}
        r = requests.post(headersort_url,data,headers = headers)
        d = r.json()
        print('【全部公司列表热度最低公司名称、及热度值为： %s'%(d['data']['data'][0]['name']),'、%s'%(d['data']['data'][0]['stat_rank.hot_score']),'】')
        self.assertGreaterEqual(d['data']['data'][2]['stat_rank.hot_score'],d['data']['data'][1]['stat_rank.hot_score'])

    # 全部公司-表头字段-排序-热度趋势-降序DESC
    def test_hot_trend_desc(self):
        headerhot_trend_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(headerhot_trend_url,data,headers = headers)
        d = r.json()
        print('【全部公司列表热度趋势最高公司名称、及热度趋势值为： %s'%(d['data']['data'][0]['name']),'、%s'%(d['data']['data'][0]['stat_rank.hot_trend']),'】')
        self.assertGreaterEqual(d['data']['data'][0]['stat_rank.hot_trend'],d['data']['data'][1]['stat_rank.hot_trend'])

    # 全部公司-表头字段-排序-热度趋势-升序ASC
    def test_hot_trend_asc(self):
        headerhot_trend_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"asc\"]}]}"}
        r = requests.post(headerhot_trend_url,data,headers = headers)
        d = r.json()
        print('【全部公司列表热度趋势最低公司名称、及热度趋势值为： %s'%(d['data']['data'][0]['name']),'、%s'%(d['data']['data'][0]['stat_rank.hot_trend']),'】')
        self.assertGreaterEqual(d['data']['data'][2]['stat_rank.hot_trend'],d['data']['data'][1]['stat_rank.hot_trend'])

#新经济公司列表
    # 新经济公司列表
    def test_new_economy(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        print('【新经济公司数量为： %s'%(d['data']['total']),'家】')
        self.assertGreaterEqual(d['data']['total'],148)

    # 新经济公司全部字段
    def test_new_economy_all_fields(self):
        new_economy_url = url + '/api/company/search'
        data = {
            "curPage":1,
            "pageSize":20,
            "type":"new_economy",
            "sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]",
            "sub_search":"[]"
                }
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        x = len(d['data']['all_fields'])
        print('【新经济公司所有表头字段有：',x,'个】')
        self.assertEqual(x,43)

    # 新经济公司默认展示字段
    def test_new_economy_all_fields(self):
        new_economy_url = url + '/api/company/search'
        data = {
            "curPage":1,
            "pageSize":20,
            "type":"new_economy",
            "sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]",
            "sub_search":"[]"
                }
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        x = len(d['data']['show_fields'])
        print('【新经济公司所有表头字段有：',x,'个】')
        self.assertEqual(x,18)

    # 新经济公司所属领域字典
    def test_new_economy_c_industry(self):
        c_industry_url = url + '/api/insight/dict_data?type=c_industry'
        r = requests.get(c_industry_url,headers = headers)
        d = r.json()
        print('【新经济公司所属领域字典有： %s'%len(d['data']),'个不同领域】')
        self.assertEqual(len(d['data']),28)

    # 新经济公司所在地字典
    def test_new_economy_c_area(self):
        c_area_url = url + '/api/insight/dict_data?type=c_area'
        r = requests.get(c_area_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【新经济公司所在地字典有:',x ,'个一级地区】')
        self.assertEqual(x,35)

#新经济公司表头筛选、排序

    # 新经济公司-筛选—公司简称
    def test_new_economy_select_name(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"name\",\"operation\":\"includes\",\"values\":[\"阿里巴巴\"],\"type\":\"predicate\"}]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        x = d['data']['list'][0]['name']
        print('【公司简称输入阿里巴巴关键词筛选结果为:',x,'】')
        self.assertEqual(x,'阿里巴巴')

    # 新经济公司-筛选—最新市值/估值
    def test_new_economy_select_market_value(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"market_value\",\"operation\":\"gt\",\"values\":[\"100000000000\"],\"type\":\"predicate\"}]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【新经济公司列表市值/估值＞1000亿美元的公司有： ',x,'家】')
        self.assertGreaterEqual(x,4)

    #新经济公司-排序—最新市值/估值—升序—ASC
    def test_new_economy_market_valuse_asc(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"market_value\",\"sort\":\"asc\"}]","sub_search":"[]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        x0 = d['data']['list'][0]['name']
        x19 = d['data']['list'][19]['name']
        print('【新经济公司最新市值/估值最低的公司为：', x0, ' 新经济公司最新市值/估值排倒数第二十低的公司为：', x19, '】')
        self.assertEqual(r.status_code, 200)

    # 新经济公司-排序—最新市值/估值—降序—DESC
    def test_new_economy_market_valuse_desc(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        x0 = d['data']['list'][0]['name']
        x19 = d['data']['list'][19]['name']
        print('【新经济公司最新市值/估值最高公司为：', x0, ' A股公司最新市值/估值排第二十位公司为：', x19, '】')
        self.assertEqual(r.status_code, 200)

    # 新经济公司-筛选—所属领域—旅游
    def test_new_economy_select_industry(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"industry\",\"operation\":\"includes\",\"values\":[\"12\"],\"type\":\"predicate\"}]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        x0 = d['data']['list'][0]['name']
        x1 = d['data']['list'][1]['name']
        x3 = d['data']['list'][0]['industry']['label']
        print('【新经济公司列表内所属领域为旅游的公司为：',x0,x1,'】')
        self.assertEqual(x3,'旅游')

    # 新经济公司-筛选—一句话简介-旅游
    def test_new_economy_select_description(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"short_description\",\"operation\":\"includes\",\"values\":[\"旅游\"],\"type\":\"predicate\"}]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        print('【新经济公司列表一句话简介内包含“旅游”的公司为:',d['data']['list'][0]['name'],'】')
        self.assertEqual(r.status_code,200)
        #print(r.status_code)

    # 新经济公司-筛选—成立时间—大于等于2015-01-01
    def test_new_economy_select_establish_date(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"establish_date\",\"operation\":\"gte\",\"values\":[\"2015-01-01\"],\"type\":\"predicate\"}]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        print('【新经济公司列表内成立时间大于等于2015-01-01的公司有：',d['data']['total'],'家】')
        self.assertEqual(r.status_code,200)

    # 新经济公司-排序—成立时间—降序—DESC
    def test_new_economy_establish_date_desc(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"establish_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        print('【成立时间最晚的公司是：',d['data']['list'][0]['name'],'成立时间为：',d['data']['list'][0]['establish_date'],'】')
        self.assertGreaterEqual(d['data']['total'],148)

    # 新经济公司-排序—成立时间—升序—ASC
    def test_establish_date_asc(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage": 1, "pageSize": 20, "type": "new_economy",
                "sort": "[{\"field\":\"establish_date\",\"sort\":\"asc\"}]", "sub_search": "[]"}
        r = requests.post(new_economy_url, data, headers=headers)
        d = r.json()
        print('【成立时间最早的公司是：', d['data']['list'][0]['name'], '成立时间为：', d['data']['list'][0]['establish_date'], '】')
        self.assertGreaterEqual(d['data']['total'], 148)

    # 新经济公司-筛选—所在地—包含：北京市-东城区
    def test_address_select(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"establish_date\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"address\",\"operation\":\"includes\",\"values\":[20101],\"type\":\"predicate\"}]"}
        r = requests.post(new_economy_url, data, headers=headers)
        d = r.json()
        print('【新经济公司列表内所在地包含北京市—东城区的公司有：', d['data']['total'], '家】')
        self.assertEqual(d['data']['list'][0]['address'][0]['name'],'北京市')
        self.assertEqual(r.status_code, 200)

    # 新经济公司列表第二页
    def test_new_economy_curpage2(self):
        new_economy_url = url + '/api/company/search'
        data = {"curPage":2,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"establish_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(new_economy_url, data, headers=headers)
        d = r.json()
        x = len(d['data']['list'])
        print('【新经济公司列表第二页的公司有：', x, '家】')
        self.assertGreaterEqual(20,x)
        self.assertEqual(r.status_code, 200)

# A股公司

    # A股公司列表
    def test_a_stock_commany(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(a_stock_url, data, headers=headers)
        d = r.json()
        x = d['data']['total']
        print('【A股公司有：', x, '家】')
        self.assertGreaterEqual(x,3500)
        self.assertEqual(r.status_code, 200)

    # A股公司所属领域字典
    def test_a_stock_c_industry(self):
        c_industry_url = url + '/api/insight/dict_data?type=c_industry'
        r = requests.get(c_industry_url,headers = headers)
        d = r.json()
        print('【A股公司所属领域字典有： %s'%len(d['data']),'个不同领域】')
        self.assertEqual(len(d['data']),28)

    # A股公司所在地字典
    def test_a_stock_c_area(self):
        c_area_url = url + '/api/insight/dict_data?type=c_area'
        r = requests.get(c_area_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【A股公司所在地字典有:',x ,'个一级地区】')
        self.assertEqual(x,35)

    # A股公司筛选—公司简称
    def test_a_stock_select_name(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"name\",\"operation\":\"includes\",\"values\":[\"贵州茅台\"],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        x = d['data']['list'][0]['name']
        print('【A股公司简称输入贵州茅台关键词筛选结果为:',x,'】')
        self.assertEqual(x,'贵州茅台')

    # A股公司-筛选—最新市值/估值
    def test_a_stock_select_market_value(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"market_value\",\"operation\":\"gt\",\"values\":[\"100000000000\"],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【A股公司列表市值/估值＞1000亿美元的公司有： ',x,'家】')
        self.assertGreaterEqual(x,9)

    # A股公司-排序—最新市值/估值—升序—ASC
    def test_a_stock_market_valuse_asc(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"asc\"}]","sub_search":"[]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        x0 = d['data']['list'][0]['name']
        x19 = d['data']['list'][19]['name']
        print('【A股公司最新市值/估值最低的公司为：', x0, ' A股公司最新市值/估值倒数第二十低的公司为：', x19, '】')
        self.assertEqual(r.status_code, 200)

    # A股公司-排序—最新市值/估值—降序—DESC
    def test_a_stock_market_valuse_desc(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        x0 = d['data']['list'][0]['name']
        x19 = d['data']['list'][19]['name']
        print('【A股公司最新市值/估值最高的公司为：', x0, ' A股公司最新市值/估值排第二十的公司为：', x19, '】')
        self.assertEqual(r.status_code, 200)

    # A股公司-筛选—所属领域—旅游
    def test_a_stock_select_industry(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"industry\",\"operation\":\"includes\",\"values\":[\"12\"],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        x0 = d['data']['total']
        #x1 = d['data']['list'][1]['name']
        x2 = d['data']['list'][0]['industry']['label']
        print('【A股公司列表内所属领域为旅游的公司为：',x0,'家】')
        self.assertEqual(x2,'旅游')

    # A股公司-筛选—一句话简介-旅游
    def test_a_stock_select_description(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"short_description\",\"operation\":\"includes\",\"values\":[\"旅游\"],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        print('【A股公司列表一句话简介内包含“旅游”的公司有:',d['data']['total'],'家】')
        self.assertEqual(r.status_code,200)

    # A股公司-筛选—成立时间—大于等于2015-01-01
    def test_a_stock_select_establish_date(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"establish_date\",\"operation\":\"gte\",\"values\":[\"2015-01-01\"],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        print('【A股公司列表内成立时间大于等于2015-01-01的公司有：',d['data']['total'],'家】')
        self.assertEqual(r.status_code,200)

    # A股公司-排序—成立时间—降序—DESC
    def test_a_stock_establish_date_desc(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"establish_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        print('【A股成立时间最晚的公司是：',d['data']['list'][0]['name'],'成立时间为：',d['data']['list'][0]['establish_date'],'】')
        self.assertEqual(r.status_code, 200)

    # A股公司-排序—成立时间—升序序—ASC
    def test_a_stock_establish_date_asc(self):
        a_stock_url= url + '/api/company/search'
        data = {"curPage": 1, "pageSize": 20, "type": "a_stock",
                "sort": "[{\"field\":\"establish_date\",\"sort\":\"asc\"}]", "sub_search": "[]"}
        r = requests.post(a_stock_url,data, headers=headers)
        d = r.json()
        print('【A股成立时间最早的公司是：', d['data']['list'][0]['name'], '成立时间为：', d['data']['list'][0]['establish_date'], '】')
        self.assertGreaterEqual(d['data']['total'], 3500)

    # A股公司-筛选—所在地—包含：北京市-东城区
    def test_a_stock_select_address(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"establish_date\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"address\",\"operation\":\"includes\",\"values\":[20101],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url, data, headers=headers)
        d = r.json()
        print('【A股公司列表内所在地包含北京市—东城区的公司数有：', d['data']['total'], '家】')
        self.assertEqual(d['data']['list'][0]['address'][0]['name'],'北京市')
        self.assertEqual(r.status_code, 200)

    # A股公司列表第二页
    def test_a_stock_curpage2(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":2,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"establish_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(a_stock_url, data, headers=headers)
        d = r.json()
        x = len(d['data']['list'])
        print('【A股公司列表第二页的公司有：', x, '家】')
        self.assertGreaterEqual(20,x)
        self.assertEqual(r.status_code, 200)

# 新三板公司

    # 新三板公司列表
    def test_nq_stock_commany(self):
        nq_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"nq_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(nq_stock_url, data, headers=headers)
        d = r.json()
        x = d['data']['total']
        print('【新三板公司数为：', x, '家】')
        self.assertGreaterEqual(x,10000)
        self.assertEqual(r.status_code, 200)

    # 新三板公司所属领域字典
    def test_nq_stock_c_industry(self):
        c_industry_url = url + '/api/insight/dict_data?type=c_industry'
        r = requests.get(c_industry_url,headers = headers)
        d = r.json()
        print('新三板公司所属领域字典有： %s'%len(d['data']),'个不同领域')
        self.assertEqual(len(d['data']),28)

    # 新三板公司所在地字典
    def test_nq_stock_c_area(self):
        c_area_url = url + '/api/insight/dict_data?type=c_area'
        r = requests.get(c_area_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【新三板公司所在地字典有:',x ,'个一级地区】')
        self.assertEqual(x,35)

    # 新三板公司-筛选—公司简称
    def test_nq_stock_select_name(self):
        nq_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"nq_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"name\",\"operation\":\"includes\",\"values\":[\"神州优车\"],\"type\":\"predicate\"}]"}
        r = requests.post(nq_stock_url,data,headers = headers)
        d = r.json()
        x = d['data']['list'][0]['name']
        print('【公司简称输入神州优车关键词筛选结果为:',x,'】')
        self.assertEqual(x,'神州优车')

    # 新三板公司-筛选—最新市值/估值—大于10亿美元
    def test_nq_stock_select_market_value(self):
        nq_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"nq_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"market_value\",\"operation\":\"gt\",\"values\":[\"1000000000\"],\"type\":\"predicate\"}]"}
        r = requests.post(nq_stock_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【新三板公司列表市值/估值＞10亿美元的公司有： ',x,'家】')
        self.assertGreaterEqual(x,9)

    # 新三板公司-排序—最新市值/估值—升序—ASC
    def test_nq_stock_market_valuse_asc(self):
        nq_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"nq_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"asc\"}]","sub_search":"[]"}
        r = requests.post(nq_stock_url,data,headers = headers)
        d = r.json()
        x0 = d['data']['list'][0]['name']
        x19 = d['data']['list'][19]['name']
        print('【新三板公司最新市值/估值升序第一位公司市值为：',x0,' 新三板公司最新市值/估值升序第二十位公司市值为：',x19,'】')
        self.assertEqual(r.status_code,200)

    # 新三板公司-排序—最新市值/估值—降序—DESC
    def test_nq_stock_market_valuse_desc(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        x0 = d['data']['list'][0]['market_value']['value_usd']
        x19 = d['data']['list'][19]['market_value']['value_usd']
        print('【A股公司最新市值/估值降序第一位公司市值为：',x0,'美元 ',' 新经济公司最新市值/估值升序第二十位公司市值为：',x19,'美元】')
        self.assertGreaterEqual(len(d['data']['list'][0]),len(d['data']['list'][19]))

    # 新三板公司-筛选—所属领域—旅游
    def test_nq_stock_select_industry(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"industry\",\"operation\":\"includes\",\"values\":[\"12\"],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        x0 = d['data']['total']
        #x1 = d['data']['list'][1]['name']
        x2 = d['data']['list'][0]['industry']['label']
        print('【A股公司列表内所属领域为旅游的公司为：',x0,'家】')
        self.assertEqual(x2,'旅游')

    # 新三板公司-筛选—一句话简介-旅游
    def test_nq_stock_select_description(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"short_description\",\"operation\":\"includes\",\"values\":[\"旅游\"],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        print('【A股公司列表一句话简介内包含“旅游”的公司为:',d['data']['total'],'家】')
        self.assertEqual(r.status_code,200)

    # A股公司-筛选—成立时间—大于等于2015-01-01
    def test_a_stock_select_establish_date(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"establish_date\",\"operation\":\"gte\",\"values\":[\"2015-01-01\"],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        print('【A股公司列表内成立时间大于等于2015-01-01的公司数有：',d['data']['total'],'家】')
        self.assertEqual(r.status_code,200)

    # A股公司-排序—成立时间—降序—DESC
    def test_a_stock_establish_date_desc(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"establish_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(a_stock_url,data,headers = headers)
        d = r.json()
        print('【A股成立时间最晚的公司是：',d['data']['list'][0]['name'],'成立时间为：',d['data']['list'][0]['establish_date'],'】')
        self.assertEqual(r.status_code, 200)

    # A股公司-排序—成立时间—升序序—ASC
    def test_a_stock_establish_date_asc(self):
        a_stock_url= url + '/api/company/search'
        data = {"curPage": 1, "pageSize": 20, "type": "a_stock",
                "sort": "[{\"field\":\"establish_date\",\"sort\":\"asc\"}]", "sub_search": "[]"}
        r = requests.post(a_stock_url,data, headers=headers)
        d = r.json()
        print('【A股成立时间最早的公司是：', d['data']['list'][0]['name'], '成立时间为：', d['data']['list'][0]['establish_date'], '】')
        self.assertGreaterEqual(d['data']['total'], 3500)

    # A股公司-筛选—所在地—包含：北京市-东城区
    def test_a_stock_select_address(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"establish_date\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"address\",\"operation\":\"includes\",\"values\":[20101],\"type\":\"predicate\"}]"}
        r = requests.post(a_stock_url, data, headers=headers)
        d = r.json()
        print('【A股公司列表内所在地包含北京市—东城区的公司数有：', d['data']['total'], '家】')
        self.assertEqual(d['data']['list'][0]['address'][0]['name'],'北京市')
        self.assertEqual(r.status_code, 200)

    # A股公司列表第二页
    def test_a_stock_curpage2(self):
        a_stock_url = url + '/api/company/search'
        data = {"curPage":2,"pageSize":20,"type":"a_stock","sort":"[{\"field\":\"establish_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(a_stock_url, data, headers=headers)
        d = r.json()
        x = len(d['data']['list'])
        print('【A股公司列表第二页的公司数有：', x, '家】')
        self.assertGreaterEqual(20,x)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()