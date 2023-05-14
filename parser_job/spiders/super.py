import scrapy
from scrapy.http import HtmlResponse
import re
from parser_job.items import ProjectParserHhItem


class SuperSpider(scrapy.Spider):
    name = 'super'
    allowed_domains = ['www.superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/programmist.html?'
                  'geo%5Bt%5D%5B0%5D=4']

    def parse(self, response):
        next_page = response.xpath('//a[@class="_1IHWd _6Nb0L _37aW8 _17KD8 '
                                   'f-test-button-dalshe f-test-link-Dalshe"]'
                                   '/@href').get()
        print(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//span[@class='_1c5Bu _1Yga1 _1QFf5 "
                                         "_2MAQA _1m76X _3UZoC _3zdq9 _1_71a']"
                                         "/a/@href").getall()

        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        vacancy_name = response.css('h1::text').get()
        vacancy_url = response.url
        vacancy_salary = response.xpath("//span[@class='_2eYAG _1m76X _3UZoC "
                                        "_3iH_l']/text()").getall()

        salary_str = ''.join(vacancy_salary)

        min_salary, max_salary = 0, 0
        salary = re.findall(r'\d+', re.sub(r'\s', '', salary_str))
        if len(salary) == 0:
            min_salary = max_salary = 'з/п не указана'
        elif len(salary) == 1:
            min_salary = max_salary = salary[0]
        elif len(salary) == 2:
            min_salary, max_salary = salary
        yield ProjectParserHhItem(name=vacancy_name, url=vacancy_url,
                                  min_salary=min_salary, max_salary=max_salary)
