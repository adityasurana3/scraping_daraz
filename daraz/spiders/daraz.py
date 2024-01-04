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
    start_urls = ['https://www.daraz.com.np/mens-clothing/?ajax=true&page=1']

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='/home/aditya/Downloads/chromedriver-linux64/chromedriver')
        self.driver.headless = True

    def parse(self, response):
        datas = json.loads(response.text)['mods']['listItems']
        for data in datas[:5]:
            name = data.get('name')
            rating = data.get('ratingScore','')
            product_url = 'https:'+data.get('productUrl','')
            yield scrapy.Request(url=product_url, callback=self.parse_data, cb_kwargs={'name':name, 'rating':rating})

    def parse_data(self, response, name, rating):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review-item")))
        # with open('index.html','a') as f:
        #     f.write(self.driver.page_source)
        total_number_review = self.driver.find_elements(By.CLASS_NAME, "ant-pagination-item")
        review =[review.text for review in total_number_review]
        total_review =int(review[-1])
        review = []
        for i in range(1,total_review):
            self.driver.execute_script(f"document.querySelector('.ant-pagination-item-{i}').click()")
            time.sleep(0.5)
            reviews = self.driver.find_elements(By.XPATH, "//div[@class='review-content-sl']")
            review.append([review.text for review in reviews])

        yield {
            'name':name,
            'rating':rating,
            'review': review
        }
        
        





# document.getElementById('rc_select_1_list_4').click()
#