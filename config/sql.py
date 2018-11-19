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
def bannerid(database='jingdata_saas'):
    #global c
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
