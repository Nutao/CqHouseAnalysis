# coding:UTF-8
__author__ = 'CZG'

import requests
from bs4 import BeautifulSoup
import re

# ץȡ���е�����ҳ��urls
citys = ['jiangbei','yubei','nanan','banan','shapingba','jiulongpo','yuzhong','dadukou',
         'jiangjing']
urls = []
# ����forѭ����������������������
for i in citys:
    url = 'http://cq.lianjia.com/ershoufang/%s/' %i
    res = requests.get(url) # ����get����
    res = res.text.encode(res.encoding).decode('utf-8') # ��Ҫת�룬�����������
    soup = BeautifulSoup(res,'html.parser') # ʹ��bs4ģ�飬����Ӧ������Դ�������html����
    page = soup.findAll('div',{'class':'page-box house-lst-page-box'}) # ʹ��finalAll��������ȡָ����ǩ�������µ�����

    #ƥ�����ҳ��
    p = str(page[0])
    # print(p)
    total = re.findall(r'\d\d',p)
    total_pages = int(total[0])
    for j in list(range(1,total_pages+1)): # ƴ��������Ҫ���������
        urls.append('http://cq.lianjia.com/ershoufang/%s/pg%s' %(i,j))

# ����csv�ļ������ں���ı�������
file = open('lianjia.csv','w',encoding = 'utf-8')

for url in urls:
    res = requests.get(url)
    res = res.text.encode(res.encoding).decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    find_all = soup.find_all(name = 'div', attrs = {'class':'info clear'})
    
    print(len(find_all))
    
    for i in list(range(len(find_all))): # ����forѭ����ץȡ������ĸ����ֶ���Ϣ
        res2 = find_all[i]

        room_type = res2.find_all('div',{'class':'houseInfo'})[0].text # ÿ�׶��ַ��Ļ���

        # ����С�����֣����ͣ����������װ�����ͣ��Ƿ��е���
        roomInfo =[i.strip() for i in room_type.split('|')]
        # �����б����ʽ��ɾ���ַ�������λ�ո�
        info = res2.find_all('div',{'class':'positionInfo'})[0].text
        info =[i.strip() for i in info.split('-')]  #�з��ַ��� ['��¥��(��28��)2011�꽨��¥', '�����']
#         louc = re.findall(r'(.¥��).*?(\d\d\d\d)',info[0])  #[('��¥��', '2011')]
#         print(louc)
        louceng = info[0]  #¥��
#         builddate = louc[0][1]  #����ʱ��
        region = info[1]  #��������
        # ÿ�׶��ַ����ܼ�
        price = find_all[i].find('div',{'class':'totalPrice'}).text[:2]
        # ÿ�׶��ַ���ƽ�����ۼ�
        price_union = find_all[i].find('div',{'class':'unitPrice'}).get("data-price")
        
        # ��������Ϣ���ܵ�һ��list��
        roomInfo.append(louceng)
#         roomInfo.append(builddate)
        roomInfo.append(region)
        roomInfo.append(price)
        roomInfo.append(price_union)
        print(roomInfo)
        for i in roomInfo:
            file.write(i)
            file.write(',')
        file.write('\n')
file.close()