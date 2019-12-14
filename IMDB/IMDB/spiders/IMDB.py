import scrapy

class QuotesSpider(scrapy.Spider):
    name = "imdb"
    start_urls = [
        'https://www.imdb.com/chart/top?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=37DEN9MHVT2SV2EDVS3F&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_3',
    ]

    def parse(self, response):
        for film in response.css('td.titleColumn a::attr(href)').getall():
            link = f'https://www.imdb.com/{film}'
            yield response.follow(link, callback=self.parse_film)
    
    def parse_film(self, response):
        data = {}
        data['title'] = response.css('h1::text').extract_first().strip()
        data['rating_value'] = response.css('div.ratingValue strong span::text').extract_first()
        data['rating_count'] = response.css('div.imdbRating a span::text').extract_first()
        data['rated'] = response.css('div.subtext::text').extract_first().split('\n')[1].strip()
        data['duration'] = response.css('div.subtext time::text').extract_first().strip()
        data['genre'] = response.css('div.subtext a::text').getall()[:-1]
        data['date'] = response.css('div.subtext a::text').getall()[-1].split(' (')[0]
        data['country'] = response.css('div.subtext a::text').getall()[-1].split('(')[1].split(')')[0]
        data['summary'] = response.css('div.summary_text::text').get().strip()
        data['directors'] = response.xpath(
            "//div[contains(@class, 'credit_summary_item') and contains(.//h4, 'Director')]/a/text()").extract() or None
        data['writers'] = response.xpath(
            "//div[contains(@class, 'credit_summary_item') and contains(.//h4, 'Writers')]/a/text()").extract() or None
        data['stars'] = response.xpath(
            "//div[contains(@class, 'credit_summary_item') and contains(.//h4, 'Stars')]/a/text()").extract() or None
        try:
            data['metascore'] = response.css('div.metacriticScore span::text').get()
        except:
            data['metascore']=''
        try:
            data['reviews'] = response.xpath("//span[contains(@class, 'subText') and contains(.//a, 'user')]/a/text()").extract()[0].split(' ')[0]
        except:
            data['reviews'] = ''
        try:
            data['critic'] = response.xpath("//span[contains(@class, 'subText') and contains(.//a, 'user')]/a/text()").extract()[1].split(' ')[0]
        except:
            data['critic']=''
        try:
            data['popularity'] = response.xpath("//div[contains(@class, 'titleReviewBarSubItem') and contains(.//div, 'Popularity')]/div/span/text()").extract_first().strip().split('\n')[0]
        except:
            data['popularity']=''
        
        yield data
    