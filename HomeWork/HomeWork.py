import time
import random
import requests
import csv
import sqlite3
import matplotlib.pyplot as plt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}
f = open('冲锋衣',mode='a',encoding='gbk',newline='')
csv_writer = csv.writer(f)
# csv_writer.writerow(['类型颜色','尺码大小'])
for page in range(0,61):
    print(f'------------正在爬取第{page}页------------')
    url = f'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1708478917668&loginType=3&uuid=181111935.1708401369416636111560.1708401369.1708401369.1708478913.2&productId=100032139847&score=0&sortType=5&page={page}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='
    response = requests.get(url=url,headers=headers)
    json_data = response.json()
    comment_list = json_data['comments']
    for comment in comment_list:
        productColor = comment['productColor']  #类型颜色
        productSize = comment['productSize']    #尺码大小
        print(productColor,productSize)
        csv_writer.writerow([productColor,productSize])
    time.sleep(random.randint(3,5))

#将csv文件导入SQLite中
conn = sqlite3.connect('Jacket.db')
cs = conn.cursor()
try:
    cs.execute('''create table books(
                productColor text,
                productSize text    
    )''')
    myJacket_list = []
    with open('Jacket.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            cs.execute(f'insert into books values("{row[0]}","{row[1]}")')
except:
    # 定义尺码对应的身高字典
    size_to_height = {
        'XS': 155,
        'S': 160,
        'M': 165,
        'L': 170,
        'XL': 180,
        'XXL': 185,
        'XXXL': 190
    }
    # 初始化男女身高列表
    male_heights = []
    female_heights = []
    data = cs.execute('select * from books')
    # 遍历数据记录
    for item in data:
        if '男' in item[0]:
            male_heights.append(size_to_height[item[1]])
        elif '女' in item[0]:
            female_heights.append(size_to_height[item[1]])
    # 计算男女平均身高
    avg_male_height = sum(male_heights) / len(male_heights)
    avg_female_height = sum(female_heights) / len(female_heights)
    print("男性平均身高：", avg_male_height)
    print("女性平均身高：", avg_female_height)
conn.commit()
conn.close()