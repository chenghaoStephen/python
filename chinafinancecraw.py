# -*- coding: utf-8 -*-

import urllib.request
import sys
from lxml import etree
import importlib
importlib.reload(sys)

def get_data_from_url(geturl, isShowHeader):
    head = {'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'}
    request = urllib.request.Request(geturl, headers=head);
    response = urllib.request.urlopen(request);
    pageCode = response.read().decode('utf-8')
    
    tree = etree.HTML(pageCode)
    if not isShowHeader:
        items = tree.xpath("//div[@class='TableList']/table/tr[@class='TextTitle']/td")
        for item in items:
            f.writelines(item.xpath("a/text() | text()")[0] + ',')
        f.writelines('\n')
    
    itemsdata = tree.xpath("//div[@class='TableList']/table/tr[not(@class='TextTitle')]")
    for tritem in itemsdata:
        for tditem in tritem.xpath("td"):
            f.writelines(tditem.xpath("node()/text() | text()")[0] + ',')
        f.writelines('\n')

    pageitems = tree.xpath("//ul[@class='page1']/li/a")
    for pageitem in pageitems:
        if pageitem.text == "下一页":
            nexturl = pageitem.get('href')
            index = nexturl.find('page=')
            nextpage = nexturl[index + 5:]
            return int(nextpage)     
    return -1


f = open('test', 'w', encoding='gbk')
curpage = 1
isShowHeader = False
url = "http://app.finance.china.com.cn/stock/list.php";
while curpage > 0:
    values = {
      "type":"ha",
      "field":"chg_pct",
      "order":"desc",
      "page":str(curpage)
    }
    data = urllib.parse.urlencode(values)
    geturl = url + "?" + data
    curpage = get_data_from_url(geturl, isShowHeader)
    isShowHeader = True


f.close()