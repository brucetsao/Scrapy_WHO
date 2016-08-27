import scrapy
from bs4 import BeautifulSoup
from who.items import WhoItem


class whoCrawler(scrapy.Spider):
    name = 'who'
    start_urls = ['http://www.whocc.no/atc_ddd_index/?code=A','http://www.whocc.no/atc_ddd_index/?code=B','http://www.whocc.no/atc_ddd_index/?code=C'
    ,'http://www.whocc.no/atc_ddd_index/?code=C','http://www.whocc.no/atc_ddd_index/?code=D','http://www.whocc.no/atc_ddd_index/?code=E'
    ,'http://www.whocc.no/atc_ddd_index/?code=F','http://www.whocc.no/atc_ddd_index/?code=G','http://www.whocc.no/atc_ddd_index/?code=H'
    ,'http://www.whocc.no/atc_ddd_index/?code=I','http://www.whocc.no/atc_ddd_index/?code=J','http://www.whocc.no/atc_ddd_index/?code=K'
    ,'http://www.whocc.no/atc_ddd_index/?code=L','http://www.whocc.no/atc_ddd_index/?code=M','http://www.whocc.no/atc_ddd_index/?code=N'
    ,'http://www.whocc.no/atc_ddd_index/?code=O','http://www.whocc.no/atc_ddd_index/?code=P','http://www.whocc.no/atc_ddd_index/?code=Q'
    ,'http://www.whocc.no/atc_ddd_index/?code=R','http://www.whocc.no/atc_ddd_index/?code=S','http://www.whocc.no/atc_ddd_index/?code=T'
    ,'http://www.whocc.no/atc_ddd_index/?code=U','http://www.whocc.no/atc_ddd_index/?code=V','http://www.whocc.no/atc_ddd_index/?code=W'
    ,'http://www.whocc.no/atc_ddd_index/?code=X','http://www.whocc.no/atc_ddd_index/?code=Y','http://www.whocc.no/atc_ddd_index/?code=Z'
    ]

    def parse(self, response):
        res = BeautifulSoup(response.body)
        domain = 'http://www.whocc.no/atc_ddd_index/'
        for news in res.select('p b'):
            # print(news.select('h1')[0].text)
            print(domain + news.select('a')[0]['href'][2:])
            yield scrapy.Request(domain + news.select('a')[0]['href'][2:], self.parse_second)

    def parse_second(self, response):
        res = BeautifulSoup(response.body)

        domain = 'http://www.whocc.no/atc_ddd_index/'
        for news2 in res.select('p b'):
            print(domain + news2.select('a')[0]['href'][2:])
            
            yield scrapy.Request(domain + news2.select('a')[0]['href'][2:], self.parse_third)
        
    def parse_third(self, response):
        res = BeautifulSoup(response.body)
        # appleItem = WhoItem()
        domain = 'http://www.whocc.no/atc_ddd_index/'
        for news3 in res.select('p b'):
            print(domain + news3.select('a')[0]['href'][2:])
            yield scrapy.Request(domain + news3.select('a')[0]['href'][2:], self.parse_detail)


    def parse_detail(self, response):
        res = BeautifulSoup(response.body)
        simpleList = []
        tmpStr = "start: --------"
        for code in res.select('tr'):
            c = code.select('td')[0].text
            name = code.select('td')[1].text
            #print(c + "," + name)
            #tmpStr = c + "," + name
            item = WhoItem()
            if(c!='ATC code'):
                item['codeW']=c
            if(name!=''):
                item['nameW']=name
            if(c!='ATC code' and name!='' ):
                simpleList.append(item)
        return simpleList
        #for name in res.select('td a'):
            #print(name.text)
            #tmpStr = name.text
        
        