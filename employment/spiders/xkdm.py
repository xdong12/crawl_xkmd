#!/usr/bin/env python3
# coding: utf-8
# Time: 2020/11/20 17:01
# Author: xd

import re
import scrapy
from employment.settings import HEADERS


class XkdmSpider(scrapy.Spider):
    """第三轮学科评估"""
    name = 'xkdm'
    allowed_domains = ['edu.cn']
    # start_urls可以设置多个
    start_urls = ['http://www.cdgdc.edu.cn/xwyyjsjyxx/sy/glmd/267001.shtml']


    # redis_key = 'ranking:start_urls'  # redis_key,用于在redis 添加起始url
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": HEADERS
    }

    def parse(self, response):
        url = response.url
        tr_list = response.xpath('//tr')
        tr_list.pop(0)
        tr_list.pop()
        item = {}
        for tr in tr_list:
            td_list = tr.xpath('./td')
            l = len(td_list)
            if l == 4:
                item['学科门类代码'] = td_list[0].xpath('./p/strong[1]/text()').extract_first()
                item['学科门类名称'] = td_list[0].xpath('./p/strong[2]/text()').extract_first()
                yjxk = td_list[1].xpath('./p/text()').extract_first()
                # item['一级学科名称'] = re.search(r'[\u4e00-\u9fa5]+', yjxk).group(0)
                # item['一级学科代码'] = re.search('[0-9]+', yjxk).group(0)
                code = re.search('[0-9]+', yjxk).group(0)
                item['一级学科代码'] =code
                item['一级学科名称'] = yjxk.replace(code, '').strip()
                item['二级学科名称'] = td_list[3].xpath('./p/text()').extract_first()
                item['二级学科代码'] = td_list[2].xpath('./p/text()').extract_first()
            elif l == 3:
                yjxk = td_list[0].xpath('./p/text()').extract_first()
                code = re.search('[0-9]+', yjxk).group(0)
                item['一级学科代码'] = code
                item['一级学科名称'] = yjxk.replace(code, '').strip()
                item['二级学科名称'] = td_list[2].xpath('./p/text()').extract_first()
                item['二级学科代码'] = td_list[1].xpath('./p/text()').extract_first()
            elif l == 2:
                item['二级学科名称'] = td_list[1].xpath('./p/text()').extract_first()
                item['二级学科代码'] = td_list[0].xpath('./p/text()').extract_first()
            if item['二级学科名称'] == '★':
                item['二级学科名称'] =''
            item['url'] = url
            item['来源'] = '学科目录'
            yield item

