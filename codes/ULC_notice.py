import sys
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import time


# 爬取南大青年的公告通知，保存标题，时间，链接3部分内容
# 读入url输出页面内容
def grab_information(url):
    r = requests.get(url)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        return r.text
    else:
        print("无法爬取网页信息")
        sys.exit(0)


# 读入网页源码，输出信息列表
# 将通知标题、时间、链接汇总成列表输出
def parse(html_page, records_per_page):
    main_text = html_page.split('<div frag="窗口6" portletmode="simpleList">')[1].split(' <div id="wp_paging_w6"> ')[0]
    soup = BeautifulSoup(main_text, 'html.parser')
    list_info = []
    tag_li = soup.li
    for i in range(records_per_page):
        href = tag_li.a.get('href')
        if "/page.htm" in href:
            href = "https://tuanwei.nju.edu.cn" + href
        title = tag_li.a.string
        p_time = tag_li.span.find_next_sibling().string
        list_info.append([title, p_time, href])
        tag_li = tag_li.find_next_sibling()
    return list_info


# 从网页提取总页面数、总记录数，每页记录数
# 读入网页，输出总页面数、总记录数,每页记录数
def parse_pcm(html):
    pcm_text = html.split('<ul class="wp_paging clearfix"> ')[1].split('<li class="page_nav">')[0]
    pcm_soup = BeautifulSoup(pcm_text, 'html.parser')
    records_per_page = int(pcm_soup.em.string)
    total_records = int(pcm_soup.span.find_next_sibling().em.string)
    total_pages = int(total_records) // int(records_per_page) + 1
    return total_pages, total_records, records_per_page


# 列表信息以xlsx表格的形式存储
# 读入列表，输出xlsx表格总记录条数
# 表格要求有标题
# 1-4列分别是序号，通知标题，发布时间，网页链接
def storage(info_list):
    #标题
    chart_title = '南大青年网站公告通知'
    c_time = "创建时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    xls2 = xlsxwriter.Workbook(chart_title + " " + time.strftime("%Y%m%d", time.localtime()) + '.xlsx')
    sht1 = xls2.add_worksheet()
    # 添加字段
    sht1.write(0, 0, chart_title)
    sht1.write(1, 0, c_time)
    sht1.write(2, 0, '序号')
    sht1.write(2, 1, '标题')
    sht1.write(2, 2, '时间')
    sht1.write(2, 3, '网址')
    # 给字段中加值   使用循环
    for i in range(len(info_list)):
        sht1.write(i + 3, 0, i + 1)
        sht1.write(i + 3, 1, info_list[i][0])
        sht1.write(i + 3, 2, info_list[i][1])
        sht1.write(i + 3, 3, info_list[i][2])
    xls2.close()


def main():
    first_url = 'https://tuanwei.nju.edu.cn/ggtz/list1.htm'
    url_prefix, url_suffix = first_url.split("1")
    html = grab_information(first_url)
    #先从第一个页面爬取总记录数，总页数，
    total_pages, total_records, records_per_page = parse_pcm(html)
    print('已爬取基本信息')
    info_list = parse(html, records_per_page)
    print('------------------已解析第1页内容--------------------')
    for i in range(2, total_pages):
        url = url_prefix + str(i) + url_suffix
        html = grab_information(url)
        info_list += parse(html, records_per_page)
        print('------------------已解析第' + str(i) + '页内容--------------------')
    url = url_prefix + str(total_pages) + url_suffix
    html = grab_information(url)
    info_list += parse(html, total_records - (total_pages - 1) * records_per_page)
    # 判断info_list中的条目数是否与总记录数相等，有问题就重新爬取
    if len(info_list) != total_records:
        print('--------------------总数异常，将重新爬取内容-------------------------')
        main()
    else:
        print('------------------总数核对无误，正在将内容存入表格---------------------')
        storage(info_list)
        print('存储完成')


if __name__ == '__main__':
    main()
