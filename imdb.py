# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 18:44:50 2019

@author: Acer
"""
from selenium import webdriver
import pandas as pd

chrome_path = r"D:\mitra\MAGANG\Selenium\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_path)

driver.get('https://www.imdb.com/chart/top?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=37DEN9MHVT2SV2EDVS3F&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_3')

titles = driver.find_elements_by_xpath('//td[@class="titleColumn"]/a')

titles_href = []
for v in range(len(titles)):
    href = titles[v].get_attribute('href')
    titles_href.append(href)
    
total = []
for v in range(len(titles_href)):
    driver.get(titles_href[49])
    title = driver.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1').text.split('(')[0]
    rating_value = driver.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span').text
    rating_count = driver.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/a/span').text
    rated = driver.find_element_by_class_name('subtext').text.split(' | ')[0]
    duration = driver.find_element_by_class_name('subtext').text.split(' | ')[1]
    genre = driver.find_element_by_class_name('subtext').text.split(' | ')[2]
    date = driver.find_element_by_class_name('subtext').text.split(' | ')[3].split(' (')[0]
    country = driver.find_element_by_class_name('subtext').text.split(' | ')[3].split(' ')[-1].replace("(","").replace(")",'')
    summary = driver.find_element_by_class_name('summary_text').text
    directors = driver.find_elements_by_class_name('credit_summary_item')[0].text.split(': ')[1]
    writers = driver.find_elements_by_class_name('credit_summary_item')[1].text.split(': ')[1]
    stars = driver.find_elements_by_class_name('credit_summary_item')[2].text.split(': ')[1]
    try:
        metascore = driver.find_element_by_class_name('metacriticScore').text
        reviews = driver.find_elements_by_class_name('subText')[1].text.split(' ')[0]
        critics = driver.find_elements_by_class_name('subText')[1].text.split(' ')[3]
        popularity = driver.find_elements_by_class_name('subText')[2].text.split(' ')[0]
    except:
        reviews = driver.find_element_by_class_name('titleReviewBar').text.split('\n')[1].split(' ')[0]
        critics = driver.find_element_by_class_name('titleReviewBar').text.split('\n')[1].split(' ')[3]
        popularity = driver.find_element_by_class_name('titleReviewBar').text.split('\n')[3].split(' ')[0]
    new = ((title, rating_value, rating_count, rated, duration, genre, date, country, summary, directors, writers,
            stars, metascore, reviews, critics, popularity))
    total.append(new)

df = pd.DataFrame(total, columns=['title', 'rating_value', 'rating_count', 'rated', 'duration', 'genre', 'date', 'country', 
                                  'summary', 'directors', 'writers','stars', 'metascore', 'reviews', 'critics', 'popularity'])