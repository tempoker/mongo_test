#2018-01-20 17:24:90

from pymongo import MongoClient
import pandas as pda
from matplotlib import pylab as pyl
client=MongoClient('localhost',27017)
db=client['test']
#d1 = {'name':'雪天','补丁':23,'city':'卡不见你'}
test=db['test']
#data = test.distinct('port') #获取不重复的port
datas = db.test.find({"port":"8123"}).limit(10).skip(5) #<pymongo.cursor.Cursor object at 0x0000000003940B00> 不能直接使用
#recs = test.find().count() #统计数量  #skip(n)跳过前n条记录   #find({},{"port":1,"ip":1}) #find({"port":"8123"})所有port=8123
#recs = [data for data in datas]

for rec in list(datas):
     print(rec.get('ip')) #输出15条ip的值
#print(list(datas)) #list(datas)只能出现一次，第二次为空
sql = test.find({'port':'8123'}).limit(20)
print(sql) #sql: <pymongo.cursor.Cursor object at 0x000000000579EA90>
data = pda.DataFrame(list(sql)) #list(sql)会把所有列显示出来，包括_id
#print(data.describe())
del data['_id']
print(data.describe())
data2 = data.T 
x = data2.values[0]
y = data2.values[1]
pyl.xlabel('x-ip')
pyl.ylabel('y-port')
pyl.title('mongodb')
pyl.plot(y,x,'om')
pyl.show()

''' 
from pymongo import MongoClient
from lxml import etree
import time,random,requests
from multiprocessing import Pool as ThreadPool
client = MongoClient('localhost',27017)
db = client['test']
test = db["test"]
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

def _get_info(url):
     data = requests.get(url,headers=headers,timeout=10).content.decode('utf-8','ignore')
     response = etree.HTML(data)
     try:
          ip = response.xpath('//*[@class="odd"]/td[2]/text()')
          port = response.xpath('//*[@class="odd"]/td[3]/text()')
          for i in range(len(ip)):
               ip_port = {'ip':ip[i],'port':port[i]}
               test.insert(ip_port)
     except Exception as e:
          print('一不意外：{0}'.format(e))
     time.sleep(random.random()*10)
          
if __name__=='__main__':
     url_base ='http://www.xicidaili.com/nn/{page}'
     urls = [url_base.format(page=i) for i in range(1,5)]
     a = time.time()
     pool = ThreadPool(12)
     pool.map(_get_info,urls)
     print('程序运行花费时间：{t}s'.format(t=time.time()-a))
     pool.close()
     pool.join()
                
'''
