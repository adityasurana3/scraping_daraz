import scrapy
import json
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class DarazSpider(scrapy.Spider):
    name = 'daraz'
    start_urls = [
        'https://www.daraz.com.np/mens-clothing/?ajax=true',
        'https://www.daraz.com.np/womens-clothing/?ajax=true',
        'https://www.daraz.com.np/mens-watches/?ajax=true',
        'https://www.daraz.com.np/mens-shoes/?ajax=true',
        'https://www.daraz.com.np/men-accessories/?ajax=true',
        'https://www.daraz.com.np/womens-watches/?ajax=true',
        'https://www.daraz.com.np/womens-shoes/?ajax=true',
        'https://www.daraz.com.np/womens-accessories/?ajax=true',
        'https://www.daraz.com.np/baby-gear/?ajax=true',
        'https://www.daraz.com.np/baby-toddler-toys-games/?ajax=true'
    ]
    

    def parse(self, response):
        last_page = 1
        url = response.url
        
        for i in range(1,last_page+1):
            yield scrapy.Request(f"{url}&page={i}", callback=self.parse_data)
    
    def parse_data(self, response):
        print(response.url)
        datas = json.loads(response.text)['mods']['listItems']
        categories = response.url.split('/')[3].split('-')
        if len(categories)>1:
            category = categories[0]
            sub_category = categories[1]
        else:
            category = categories[0]
            sub_category = ''
        for data in datas:
            name = data.get('name')
            rating = data.get('ratingScore','')
            images = data.get('image','')
            total_number_of_rating = data.get('review','')
            yield {
                'url': response.url,
                'name':name,
                'rating':rating,
                'category':category,
                'sub_category':sub_category,
                'images':images,
                'total_number_of_rating':total_number_of_rating,
            }
            