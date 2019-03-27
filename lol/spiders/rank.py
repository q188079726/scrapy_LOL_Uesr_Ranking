# -*- coding: utf-8 -*-
import scrapy
from lol.items import LolItem

class RankSpider(scrapy.Spider):
    name = 'rank'
    allowed_domains = ['op.gg']
    start_urls = ['https://www.op.gg/ranking/ladder/']

    def parse(self, response):
        page_number_string_node = response.xpath('//div[@class="ranking-pagination__desc"]/span[2]/text()').extract()
        page_number_string = page_number_string_node[0].replace(',','')
        page_number = int(int(page_number_string)/100+2)
        print(page_number)
        for i in range(page_number):
            yield scrapy.Request('https://www.op.gg/ranking/ladder/page='+str(i),callback=self.parse_rank) 

    def parse_rank(self, response):
        #前5名
        name_list = response.xpath("//a[@class='ranking-highest__name']/text()").extract()
        if len(name_list)>0:
            rank_list = response.xpath("//li[contains(@class,'ranking-highest__item')]/div[@class='ranking-highest__rank']/text()").extract()
            tier_list = response.xpath('//div[contains(@class,"ranking-highest__tierrank")]/span/text()').extract()
            LP_list = response.xpath('//div[contains(@class,"ranking-highest__tierrank")]/b/text()').extract()
            Level_list = response.xpath("//div[@class='ranking-highest__level']/text()").extract()
            win_list = response.xpath("//li[contains(@class,'ranking-highest__item')]/div[@class='ranking-highest-winratio']/div/div/div[@class='winratio-graph__text winratio-graph__text--left']/text()").extract()
            lost_list = response.xpath("//li[contains(@class,'ranking-highest__item')]/div[@class='ranking-highest-winratio']/div/div/div[@class='winratio-graph__text winratio-graph__text--right']/text()").extract()
            ratio_list = response.xpath("//li[contains(@class,'ranking-highest__item')]/div[@class='ranking-highest-winratio']/div/span/text()").extract()
            
            for i in range(len(name_list)):
                item = LolItem()
                item['rank'] = rank_list[i].replace('\n','').replace('\t','')
                item['name'] = name_list[i].replace('\n','').replace('\t','')
                item['tier'] = tier_list[i].replace('\n','').replace('\t','')
                item['LP'] = LP_list[i].replace('\n','').replace('\t','')
                item['level'] = Level_list[i].replace('\n','').replace('\t','')
                item['win'] = win_list[i].replace('\n','').replace('\t','')
                item['lost'] = lost_list[i].replace('\n','').replace('\t','')
                item['ratio'] = ratio_list[i].replace('\n','').replace('\t','')
                yield item
        
        #5名之后
        rank_list = response.xpath('//td[contains(@class,"ranking-table__cell--rank")]/text()').extract()
        name_list = response.xpath('//td[contains(@class,"ranking-table__cell--summoner")]/a/span/text()').extract()
        tier_list = response.xpath('//td[contains(@class,"ranking-table__cell--tier")]/text()').extract()
        LP_list = response.xpath('//td[contains(@class,"ranking-table__cell--lp")]/text()').extract()
        Level_list = response.xpath('//td[contains(@class,"ranking-table__cell--level")]/text()').extract()
        win_list = response.xpath('//td[contains(@class,"ranking-table__cell--winratio")]/div/div/div[@class="winratio-graph__text winratio-graph__text--left"]/text()').extract()
        lost_list = response.xpath('//td[contains(@class,"ranking-table__cell--winratio")]/div/div/div[@class="winratio-graph__text winratio-graph__text--right"]/text()').extract()
        ratio_list = response.xpath('//td[contains(@class,"ranking-table__cell--winratio")]/div/span/text()').extract()

        for i in range(len(rank_list)):
            item = LolItem()
            item['rank'] = rank_list[i].replace('\n','').replace('\t','')
            item['name'] = name_list[i].replace('\n','').replace('\t','')
            item['tier'] = tier_list[i].replace('\n','').replace('\t','')
            item['LP'] = LP_list[i].replace('\n','').replace('\t','')
            item['level'] = Level_list[i].replace('\n','').replace('\t','')
            item['win'] = win_list[i].replace('\n','').replace('\t','')
            item['lost'] = lost_list[i].replace('\n','').replace('\t','')
            item['ratio'] = ratio_list[i].replace('\n','').replace('\t','')
            yield item
            