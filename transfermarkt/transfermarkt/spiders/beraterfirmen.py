import scrapy
import re


class BeraterfirmenSpider(scrapy.Spider):
    name = 'beraterfirmen'
    allowed_domains = ['transfermarkt.de']
    start_urls = ['https://www.transfermarkt.de/berater/beraterfirmenuebersicht/berater']

    def parse(self, response):
        for i in list(range(1,26)):
            print('####################')
            marktwert = re.findall('\d*\,?\d+',(response.css('#yw1 > table > tbody > tr:nth-child({}) > td:nth-child(6)::text'.format(i)).extract_first()))[0].replace(',','.') if len(re.findall('\d*\,?\d+',response.css('#yw1 > table > tbody > tr:nth-child({}) > td:nth-child(6)::text'.format(i)).extract_first()))>0 else 0
            avg_markt = re.findall('\d*\,?\d+',(response.css('#yw1 > table > tbody > tr:nth-child({}) > td:nth-child(7)::text'.format(i)).extract_first()))[0].replace(',','.') if len(re.findall('\d*\,?\d+',response.css('#yw1 > table > tbody > tr:nth-child({}) > td:nth-child(7)::text'.format(i)).extract_first()))>0 else 0
            yield {
                'Beraterfirma': response.css('table.items > tbody > tr:nth-child({}) > td.links > table > tr:nth-child(1) > td > a::text'.format(i)).extract_first(),
                'Land': response.css('table.items > tbody > tr:nth-child({}) > td.links > table > tr:nth-child(2) > td::text'.format(i)).extract_first(),
                'Transfermarktlink': response.urljoin(response.css('table.items > tbody > tr:nth-child({}) > td.links > table > tr:nth-child(1) > td > a::attr(href)'.format(i)).extract_first()),
                'Spieler': response.css('#yw1 > table > tbody > tr:nth-child({}) > td:nth-child(3) > a::text'.format(i)).extract_first(),
                'Spieler 1. Liga': response.css('#yw1 > table > tbody > tr:nth-child({}) > td:nth-child(4) > a::text'.format(i)).extract_first(),
                'Gerüchte': response.css('#yw1 > table > tbody > tr:nth-child({}) > td:nth-child(5) > a::text'.format(i)).extract_first(),
                'Gesamtmarktwert in €':float(marktwert)*1000000,
                'Durchschnittlicher Marktwert in €': float(avg_markt)*1000000,
            }
        
        next_page_url = response.urljoin(response.css('#yw2 > li.naechste-seite > a::attr(href)').extract_first())
        yield scrapy.Request(next_page_url, self.parse)



class BeraterfirmenSpider(scrapy.Spider):
    name = 'beraterfirmen_info'
    allowed_domains = ['transfermarkt.de']
    start_urls = ['https://www.transfermarkt.de/berater/beraterfirmenuebersicht/berater']

    def parse(self, response):
        for i in list(range(1,26)):
            yield scrapy.Request(response.urljoin(response.css('table.items > tbody > tr:nth-child({}) > td.links > table > tr:nth-child(1) > td > a::attr(href)'.format(i)).extract_first()),self.parse_details)
        
        next_page_url = response.urljoin(response.css('#yw2 > li.naechste-seite > a::attr(href)').extract_first())
        yield scrapy.Request(next_page_url, self.parse)

    def parse_details(self, response):
        homepage_loc = len(response.css('#main > div:nth-child(11) > div > div > div.box-content > div:nth-child(4) > div > div').extract())
        loc_two = len(response.css('div.beraterfirmainfo:nth-of-type(3) > div > div').extract())

        yield {
            'Beraterfirma': response.css('#main > div:nth-child(11) > div > div > div.box-header > div::text').extract_first().rstrip("\n").rstrip("\r").strip(),
            'Webseite': response.css('#main > div:nth-child(11) > div > div > div.box-content > div:nth-child(4) > div > div:nth-child({}) > div:nth-child(2) > a::text'.format(homepage_loc)).extract_first(),
            'Webseite_2': response.css('div.beraterfirmainfo:nth-of-type(3) > div > div:nth-child({}) > div:nth-child(2) > a::text'.format(loc_two)).extract_first(),
        }
