import unittest
import requests
import json
from config.url import url,headers
from config.gl import *
import pymysql

class ProjectDetailsTest(unittest.TestCase):

    # 阿里巴巴项目详情页
    def test_company_tab(self):
        company_url = url + '/api/company/tab?cid=' + str(albb_id)
        r = requests.get(company_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【阿里巴巴详情页Tab数量为：',x,'】')
        self.assertEqual(x,10)

    def test_userinsightdata(self):
        '''阿里巴巴详情页—收藏夹'''
        userinsightdata_url = url + '/api/userscollection/userinsightdata?type=1&insight_id=' + str(albb_id)
        r = requests.get(userinsightdata_url,headers = headers)
        d = r.json()
        print('【阿里巴巴默认收藏夹—',d['data']['folder_list'][0]['name'],'】')
        self.assertEqual(r.status_code,200)

    def test_company_index(self):
        '''阿里巴巴详情页公司信息'''
        company_url = url + '/api/company/index?cid=' + str(albb_id)
        r = requests.get(company_url,headers = headers)
        d = r.json()
        x = d['data']['list']['info']['cid']
        self.assertEqual(x,str(albb_id))
        x1 = d['data']['list']['info']['establish_date']
        self.assertEqual(x1,'1999-06-27 16:00:00')
        x2 = d['data']['list']['info']['market_value']['value_usd']
        print('【阿里巴巴的最新市值是（单位：美元）',x2,'】')
        self.assertGreaterEqual(x2,300000000000)
        x3 = d['data']['list']['info']['annual_turnover']['value']
        print('【阿里巴巴的年营业（单位：美元）',x3,'】')
        self.assertGreaterEqual(x3,30000000000)

    def test_company_folder(self):
        '''公司详情页收藏夹'''
        company_folder_url = url + '/api/userscollection/userinsightdata?type=1&insight_id=' + str(albb_id)
        r = requests.get(company_folder_url,headers = headers)
        d = r.json()
        x = d['data']['folder_list'][0]['name']
        self.assertEqual(x,'我的收藏')

    def test_company_security(self):
        '''阿里巴巴详情页—证券信息'''
        company_security_url = url + '/api/company/security?cid=' + str(albb_id)
        r = requests.get(company_security_url,headers = headers)
        d = r.json()
        x = d['data']['list']['security']['total_market_value']  #总市值
        x1 = d['data']['list']['security']['total_equity']  #总股本
        x2 = d['data']['list']['security']['lot_size']  #每手股数
        x3 = len(d['data']['menu']) #证券信息左侧menu
        print('【阿里巴巴总市值：',x,'】')
        print('【阿里巴巴总股本：', x1, '】')
        print('【阿里巴巴证券信息左侧menu有：',x3,'个】')
        self.assertGreaterEqual(r.status_code,200)
        self.assertEqual(x2,1)
        self.assertEqual(x3,3)

    def test_company_security_markettrend_month3(self):
        '''阿里巴巴详情页—证券信息—近三个月股价走势'''
        markettrend_month3_url = url + '/api/company/security/markettrend?cid=' + str(albb_id) + '&month=4'
        r = requests.get(markettrend_month3_url,headers = headers)
        d = r.json()
        x0 = len(d['data']['data']['days'])  #近三个月交易天数
        x1 = len(d['data']['data']['values'])  #近三个月交易值数量
        self.assertGreaterEqual(x0,70)
        self.assertGreaterEqual(x1,70)
        self.assertEqual(x0,x1)
        if r.status_code == 200:
            print('【阿里巴巴详情页—证券信息—近三个月股价走势】')
        else:
            pass

    def test_company_security_markettrend_month6(self):
        '''阿里巴巴详情页—证券信息—近六个月股价走势'''
        markettrend_month6_url = url + '/api/company/security/markettrend?cid=' + str(albb_id) + '&month=7'
        r = requests.get(markettrend_month6_url,headers = headers)
        d = r.json()
        x0 = len(d['data']['data']['days'])  #近六个月交易天数
        x1 = len(d['data']['data']['values'])  #近六个月交易值数量
        self.assertGreaterEqual(x0,120)
        self.assertGreaterEqual(x1,120)
        self.assertEqual(x0,x1)
        if r.status_code == 200:
            print('【阿里巴巴详情页—证券信息—近六个月股价走势】')
        else:
            pass

    def test_company_security_markettrend_month12(self):
        '''阿里巴巴详情页—证券信息—近十二个月股价走势'''
        markettrend_month12_url = url + '/api/company/security/markettrend?cid=' + str(albb_id) + '&month=13'
        r = requests.get(markettrend_month12_url,headers = headers)
        d = r.json()
        x0 = len(d['data']['data']['days'])  #近十二个月交易天数
        x1 = len(d['data']['data']['values'])  #近十二个月交易值数量
        self.assertGreaterEqual(x0,240)
        self.assertGreaterEqual(x1,240)
        self.assertEqual(x0,x1)
        if r.status_code == 200:
            print('【阿里巴巴详情页—证券信息—近十二个月股价走势】')
        else:
            pass

    def test_company_security_markettrend_all(self):
        '''阿里巴巴详情页—证券信息—全部股价走势'''
        markettrend_all_url = url + '/api/company/security/markettrend?cid=' + str(albb_id) + '&month='
        r = requests.get(markettrend_all_url,headers = headers)
        d = r.json()
        x0 = len(d['data']['data']['days'])  #全部交易天数
        x1 = len(d['data']['data']['values'])  #全部交易值数量
        self.assertGreaterEqual(x0,1000)
        self.assertGreaterEqual(x1,1000)
        self.assertEqual(x0,x1)
        if r.status_code == 200:
            print('【阿里巴巴详情页—证券信息—全部股价走势】')
        else:
            pass

    def test_company_industrycommerce(self):
        '''阿里巴巴详情页—工商法务'''
        industrycommerce_url = url + '/api/company/industrycommerce?cid=' + str(albb_id)
        r = requests.get(industrycommerce_url,headers = headers)
        d = r.json()
        x0 = d['data']['list']['industrycommerce']['name']               # 阿里巴巴注册名称
        print('【阿里巴巴注册名称：',x0,'】')
        self.assertEqual(x0,'阿里巴巴（中国）有限公司')
        x1 = d['data']['list']['industrycommerce']['legal_person_name']  # 阿里巴巴法人代表
        print('【阿里巴巴法人代表：', x1, '】')
        self.assertEqual(x1, '张勇')
        x2 = d['data']['list']['industrycommerce']['reg_status']         # 阿里巴巴公司状态
        self.assertEqual(x2, '存续')
        x3 = d['data']['list']['industrycommerce']['org_number']         # 阿里巴巴组织机构代码
        self.assertEqual(x3,'799655058')
        x4 = d['data']['list']['industrycommerce']['reg_capital']        # 阿里巴巴注册资本
        self.assertEqual(x4, '15298.00万美元')
        x5 = d['data']['list']['industrycommerce']['reg_number']         # 阿里巴巴工商注册号
        self.assertEqual(x5,'330100400013364')
        x6 = d['data']['list']['industrycommerce']['estiblish_time']     # 阿里巴巴注册时间
        self.assertEqual(x6,'2007-03-26')
        x7 = d['data']['list']['industrycommerce']['property1']  # 阿里巴巴统一社会信用代码
        self.assertEqual(x7,'91330100799655058B')
        x8 = d['data']['list']['industrycommerce']['property4']  # 阿里巴巴统一纳税人识别号
        self.assertEqual(x7, '91330100799655058B')
        x9 = d['data']['list']['industrycommerce']['property3']  # 阿里巴巴英文名称
        self.assertEqual(x9,'Alibaba(China)Co.,Ltd.')
        x = len(d['data']['menu'])  # 左侧menu
        self.assertEqual(x,2)

    def test_commpany_industrycommercechange(self):
        '''阿里巴巴详情页—工商法务—工商变更'''
        industrycommercechange_url = url + '/api/company/industrycommercechange?cid=' + str(albb_id) + '&change_item=&curPage=1&pageSize=20'
        r = requests.get(industrycommercechange_url,headers = headers)
        d = r.json()
        x0 = d['data']['total']
        print('【阿里巴巴详情页—工商法务—工商变更数量：',x0,'】')
        self.assertEqual(r.status_code,200)

    def test_commpany_equitystructure(self):
        '''阿里巴巴详情页—股权结构'''
        equity_structure_url = url + '/api/company/equitystructure?cid=' + str(albb_id)
        r = requests.get(equity_structure_url,headers = headers)
        d = r.json()
        x0 = len(d['data']['menu'])
        x1 = d['data']['list']['equitystructure']['nodeDataArray'][0]['text']
        print('【阿里巴巴详情页—股权结构—最大股东为：',x1,'】')
        self.assertEqual(x0,2)
        self.assertEqual(x1,'阿里巴巴')

    def test_commpany_investment_distribution(self):
        '''阿里巴巴详情页—投资布局'''
        investment_distribution_url = url + '/api/company/investmentdistribution?cid=' + str(albb_id)
        r = requests.get(investment_distribution_url,headers = headers)
        d = r.json()
        x0 = len(d['data']['menu'])
        self.assertEqual(x0,3)
        x1 = len(d['data']['list']['investmentdistribution']['nodeDataArray']) #投资布局
        print('【阿里巴巴详情页—投资布局数量为：',x1,'】')
        self.assertGreaterEqual(x1,11)
        x2 = d['data']['list']['investmentmerge']['total']  #阿里巴巴控股子公司
        print('【阿里巴巴详情页—投资布局—控股子公司数量为：',x2,'家】')
        self.assertEqual(x2,41)
        x3 = d['data']['list']['investmentabroad']['total']  #阿里巴巴对外投资
        print('【阿里巴巴详情页—投资布局—对外投资数量为：', x3, '家】')
        self.assertEqual(x3, 302)

    def test_company_operation(self):
        '''阿里巴巴详情页—经营数据'''
        operation_url = url + '/api/company/operation?cid=' + str(albb_id)
        r = requests.get(operation_url,headers = headers)
        d = r.json()
        x0 = len(d['data']['menu'])
        self.assertEqual(x0,7)
        print('【阿里巴巴详情页—经营数据左侧menu有：',x0,'个】')
        x1 = d['data']['list']['total_count']
        print('【阿里巴巴详情页—经营数据有',x1,'个统计图】')
        self.assertEqual(x1,27)

    def test_company_operation_detail(self):
        '''阿里巴巴详情页—经营数据—全屏'''
        operation_detail_url = url + '/api/company/operation/detail?cid=' + str(albb_id) + '&id=' + str(operation_id)
        r = requests.get(operation_detail_url,headers = headers)
        d = r.json()
        x = d['msg']
        self.assertEqual(x,'成功')

    def test_operation_download(self):
        '''阿里巴巴详情页—经营数据—下载'''
        operation_download_url = url + '/api/company/operation?cid=' + str(albb_id) + '&id=' + str(operation_id)
        r = requests.get(operation_download_url,headers = headers)
        if r.status_code == 200:
            print('【阿里巴巴详情页—经营数据—下载成功】')
        else:
            print('【阿里巴巴详情页—经营数据—下载失败】')

    def test_company_finance(self):
        '''阿里巴巴详情页—财务数据'''
        finance_url = url + '/api/company/finance?cid=' + str(albb_id)
        r = requests.get(finance_url,headers = headers)
        d = r.json()
        x0 = len(d['data']['menu'])
        print('【阿里巴巴详情页—财务数据menu有：',x0,'个】')
        self.assertEqual(x0,5)

    def test_company_finance_abstract_download(self):
        '''阿里巴巴详情页—财务数据—财务摘要导出'''
        finance_download_url = url + '/api/company/finance/abstract?cid=' + str(albb_id) + '&is_export=1&report_type=-1&select_date=0&unit=100000000'
        r = requests.get(finance_download_url,headers = headers)
        if r.status_code == 200:
            print('【阿里巴巴详情页—财务数据—财务摘要导出成功】')
        else:
            pass
        self.assertEqual(r.status_code,200)

    def test_company_finance_profit_download(self):
        '''阿里巴巴详情页—财务数据—利润表导出'''
        finance_download_url = url + '/api/company/finance/abstract?cid=' + str(albb_id) + '&is_export=1&report_type=-1&select_date=1000&unit=100000000'
        r = requests.get(finance_download_url,headers = headers)
        if r.status_code == 200:
            print('【阿里巴巴详情页—财务数据—利润表导出成功】')
        else:
            pass
        self.assertEqual(r.status_code,200)

    def test_company_finance_balance_download(self):
        '''阿里巴巴详情页—财务数据—资产负债表导出'''
        finance_download_url = url + '/api/company/finance/balance?cid=' + str(albb_id) + '&is_export=1&report_type=-1&select_date=1000&unit=100000000'
        r = requests.get(finance_download_url,headers = headers)
        if r.status_code == 200:
            print('【阿里巴巴详情页—财务数据—资产负债表导出成功】')
        else:
            pass
        self.assertEqual(r.status_code,200)

    def test_company_finance_cash_flow_download(self):
        '''阿里巴巴详情页—财务数据—现金流量表导出'''
        finance_download_url = url + '/api/company/finance/cash_flow?cid=' + str(albb_id) + '&is_export=1&report_type=-1&select_date=1000&unit=100000000'
        r = requests.get(finance_download_url, headers=headers)
        if r.status_code == 200:
            print('【阿里巴巴详情页—财务数据—现金流量表导出成功】')
        else:
            pass
        self.assertEqual(r.status_code, 200)

    def test_company_finance_main_business_download(self):
        '''阿里巴巴详情页—财务数据—主营业务构成表导出'''
        finance_download_url = url + '/api/company/finance/main_business?cid=' + str(albb_id) + '&is_export=1&report_type=-1&select_date=1000&unit=100000000'
        r = requests.get(finance_download_url, headers=headers)
        if r.status_code == 200:
            print('【阿里巴巴详情页—财务数据—主营业务构成表导出成功】')
        else:
            pass
        self.assertEqual(r.status_code, 200)





if __name__ == '__main__':
    unittest.main()