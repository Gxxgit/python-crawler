# coding=utf-8
import requests
from bs4 import BeautifulSoup
import xlwt
import datetime


def search_house(title, url):
    page_html = requests.get(url, headers=Hostreferer)
    page_soup = BeautifulSoup(page_html.text, "html.parser")
    # 房屋租金
    rentPrice = page_soup.find('p', class_='content__aside--title').text
    # latitude = page_soup.find('script', class_='map__cur')['data-el']

    basicInfo = page_soup.find('p', class_='content__article__table')
    # 面积
    area = basicInfo.find_all('span')[2].text
    # 户型
    type = basicInfo.find_all('span')[1].text
    # 房屋朝向
    orient = basicInfo.find_all('span')[3].text
    # 所在楼层
    level = page_soup.find('div', class_='content__article__info').find('ul').find_all('li')[7].text
    # print(title, rentPrice)
    # 周边交通
    transportation = page_soup.find('div', class_='content__article__info4').find('ul').find_all('li')
    way = ''
    for t in transportation:
        way = way + ' ' + t.text.strip().replace(' ', '').replace('\n', '')
    # print(way)
    return [title, rentPrice, area, type, level, orient, way]


def init_excel():
    headData = ['名称', '价格', '面积', '户型', '楼层', '交通']  # 表头部信息
    for colnum in range(0, 6):
        ws.write(0, colnum, headData[colnum], xlwt.easyxf('font: bold on'))  # 行，列


def write_excel(list, lineNum):
    for i in range(0, 6):
        ws.write(lineNum, i, list[i])  # 行，列，数据


# http请求头
Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'https://nj.zu.ke.com/'
               }
url_list = []
host_url = 'https://nj.zu.ke.com'
# index_url = 'https://nj.zu.ke.com/zufang/pg1rt200600000001/'
# 初始化excel
thisTime = datetime.datetime.now().strftime('%Y%m%d')
newTable = "d:/test_" + thisTime + ".xls"  # 表格名称
wb = xlwt.Workbook(encoding='utf-8')  # 创建excel文件，声明编码
ws = wb.add_sheet('rentInfo')  # 创建表格
init_excel()
lineNum = 1
# 遍历有效目录页
for pageNum in range(1, 68):
    print('#####开始获取第'+str(pageNum)+'页数据#####')
    index_url = 'https://nj.zu.ke.com/zufang/pg' + str(pageNum) + 'rt200600000001/'
    index_html = requests.get(index_url, headers=Hostreferer)
    soup = BeautifulSoup(index_html.text, "html.parser")
    content_list = soup.find_all('div', class_='content__list--item')

    for item in content_list:
        if item.find('a', class_='link'):
            title = item.find('a', class_='content__list--item--aside')['title']
            pageUrl = host_url+item.find('a',
                                         class_='content__list--item--aside')['href']+'?nav=200600000001&layout_id='+item.find('a', class_='link')['data-id']
            # print(title, pageUrl)
            # print('nothing')
        else:
            title = item.find('a', class_='content__list--item--aside')['title']
            print('\t' + title)
            pageUrl = host_url+item.find('a', class_='content__list--item--aside')['href']
            infoAry = search_house(title, pageUrl)
            write_excel(infoAry, lineNum)
            lineNum += 1
    print('#####本页结束#####')
wb.save(newTable)
print('#####爬取结束#####')


'''
未解决的问题：
1. 地理位置如何去掉多余空行和空格（通过replace将换行符和空格去掉） solved
2. 公寓信息解析
2. 如何获取到经纬度，以及火星坐标转换
3. 保存为excel（遇到问题：每次只保留最后一条数据。发现由于每次遍历都会重新创建表单，所以将新建表单放在最外层）solved

'''
