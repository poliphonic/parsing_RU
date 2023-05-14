import scrapy
from scrapy.http import HtmlResponse
import re
from parser_job.items import ProjectParserHhItem


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'

    allowed_domains = ['hh.ru']

    start_urls = [
        'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&'
        'text=Data+science&excluded_text=&area=2&salary=&currency_code=RUR&'
        'experience=doesNotMatter&order_by=relevance&search_period=0&'
        'items_on_page=20']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//a[@class='serp-item__title']/"
                                         "@href").getall()
        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        vacancy_name = response.css('h1::text').get()
        vacancy_url = response.url
        vacancy_salary = response.xpath('//div[@data-qa="vacancy-salary"]//'
                                        'text()').getall()
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
