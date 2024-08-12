import scrapy
from chefaa.items import ChefaaItem
from logging import FileHandler
import requests
from random import randint

class MedicationSpider(scrapy.Spider):
    # API key for ScrapeOps
    SCRAPEOPS_API_KEY = '585975d6-742e-4fbf-842d-3bb33533e87d'

    # Method to get a list of user agents from ScrapeOps
    def get_user_agent_list():
        response = requests.get(f'http://headers.scrapeops.io/v1/user-agents?api_key={MedicationSpider.SCRAPEOPS_API_KEY}')
        json_response = response.json()
        return json_response.get('result', [])

    # Method to get a random user agent from the list
    def get_random_user_agent(user_agent_list):
        random_index = randint(0, len(user_agent_list) - 1)
        return user_agent_list[random_index]

    # Spider name and allowed domains
    name = "medication"
    allowed_domains = ["chefaa.com"]
    start_urls = ["https://chefaa.com/eg-en/now/category/medications"]
    
    # Custom settings for the spider
    custom_settings = {
        "DUPEFILTER_DEBUG": True
    }

    # Process request to add a random user agent to the headers
    def process_request(self, request, spider):
        user_agent = self.get_random_user_agent()
        request.headers['User-Agent'] = user_agent

    # Parse the response from the start URLs
    def parse(self, response):
        meds = response.css('div.col-6.col-md-3')
        for med in meds:
            item_url = med.css('a[itemprop=url]').attrib['href']
            yield response.follow(item_url, self.med_parse)
        
        # Follow the next page link if it exists
        next_page = response.css('a[rel=next]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    # Parse the details of each medication item
    def med_parse(self, response):
        item = ChefaaItem()
        item['name'] = response.css('h1[itemprop=name]::text').get().strip()
        item['price'] = response.css('span[itemprop=price]::text').get().strip()
        
        # Check if the brand information is available
        if len(response.css('button.nav-link').getall()) == 2:
            item['brand'] = response.css('td::text').getall()[1].strip()
        else:
            item['brand'] = "-"
        
        # Check if the medication needs a prescription
        if response.css('.need-presc-label'):
            item['prescription'] = 'Need Prescription'
        else:
            item['prescription'] = 'Without Prescription'
        
        # Check the stock status of the medication
        if response.css('.internal-low-stock'):
            item['stock'] = 'Low'
        else:
            item['stock'] = 'Normal'
        
        # Get the category and URL of the medication
        item['category'] = response.xpath('//li[@aria-current="page"]/preceding-sibling::li[1]/a/text()').get().strip()
        item['url'] = response.url
        
        yield item