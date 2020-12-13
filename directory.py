#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 20:32:39 2020

@author: guanhuali
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from queue import Queue
import operator
import time
import types
import urllib
import get_feature
import requests
import time
from bs4 import BeautifulSoup
import pickle
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import predict

def simple_enter(browser,query):
    lists = browser.find_elements_by_tag_name('input')
    for x in lists:
        text = x.get_attribute('type')
        if text == "text" or text == "search":
            x.send_keys(query)
            x.send_keys(Keys.RETURN)
            break

def click_required(browser,query):

    buttons = browser.find_elements_by_tag_name('button')
    for button in buttons:
        temp = button.text
        temp = temp.lstrip(' \n\t')
        temp = temp.rstrip(' \n\t')
        temp1 = temp.split(' ')
        if ('Search' or 'search') in temp1 or 'Menu' in temp1:
            try:
                button.click()
            except:
                break
        
    a = browser.find_elements_by_tag_name('a')
    for button in a:
        temp = button.text
        temp = temp.lstrip(' \n\t')
        temp = temp.rstrip(' \n\t')
        temp1 = temp.split(' ')
        toggle = button.get_attribute('id')
        if (button.get_attribute('role') == 'button' or  ('search' in toggle and 'toggle' in toggle))and (("Search" or "Menu") in temp1):
            button.click()
            break
            
    lists = browser.find_elements_by_tag_name('input')
    for x in lists:
        text = x.get_attribute('type')
        if text == "text" or text == "search":
            x.send_keys(query)
            x.send_keys(Keys.RETURN)
            break
        
def give_input(URL,query):
    browser = webdriver.Safari()
    try:
        browser.get(URL)
    except:
        print('no web')
    

    browser.maximize_window()
    try:
        simple_enter(browser,query)
    except:
        try:
            click_required(browser,query)
        except:
            kk =2
    
    time.sleep(1.5)
    all_web = browser.find_elements_by_tag_name('a')
    
    result = []
    count = 0
    for i in all_web:
        try:
            link = i.get_attribute('href')
        except:
            continue
        
        if link:
            distance = abs(len(link) - len(URL))
        else:
            continue
        temp = i.text
        temp = temp.lstrip(' \n\t')
        temp = temp.rstrip(' \n\t')
        temp1 = temp.split(' ')
        if link and ('Faculty' or 'Staff' or 'People') in temp1 and distance <= 50 or ('faculty' or 'directory') in link:
            result.append(link)
            count +=1
        if count == 15:
            break
    browser.close()
    return result

def google(query):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    

    query = query
    
    query = query.replace(' ', '+')
    URL = "https://google.com/search?q={" + query +"}"
    
    headers = {"user-agent": USER_AGENT}
    res = ''
    #Using time.sleep to handle exceptions
    while res == '':
        try:
            res = requests.get(URL,headers = headers)
            break
        except:
            print("i need sleep")
            time.sleep(5)
            continue
    count = 0
    if res.status_code == 200:
        soup = BeautifulSoup(res.content,"html.parser")
        results = []
        for g in soup.find_all('div',class_ = 'rc'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                # title = g.find('h3').text
                # item = {
                #     "title": title,
                #     "link": link
                # }
    
            results.append(link)
            count += 1
            if count == 3:
                break
    return results

def get_all(URL,query):
    browser = webdriver.Safari()
    try:
        browser.get(URL)
    except:
        print('no web')
     
    browser.maximize_window()
    len_URL = len(URL)
    all_candi = browser.find_elements_by_tag_name('a')
    link_list = []
    link_set = {}
    for x in all_candi:
        link = x.get_attribute('href')
        if link == None:
            continue
    
        if link in query:
            continue
        ori = abs(len(link) - len_URL)
        if ori <= 2 or 'content' in link.lower() or 'course' in link.lower() or 'research' in link.lower():
            continue
        if "http" not in link:
            continue
        link = link.rstrip('/')
        temp = link.split('/')
        if len(temp) <= 3:
            continue
        #print(temp[-1])
        if 'page' in temp[-1]:
            continue
        string = ''
        for i in range(len(temp)-1):
            string += temp[i]
            if 'http' in temp[i]:
                string += ('//')
            elif temp[i] == '':
                continue
            else:
                string +=('/')
                
        if link in link_list:
            continue
        else:
            link_list.append(link)
            
        if string in link_set:
            link_set[string] += 1
        else:
            link_set[string] = 1
    container = max(link_set.items(), key=operator.itemgetter(1))[0]
    len_con = len(container)
    final = []
    
    for j in link_list:
        len_cur = len(j)
        ori = abs(len_cur - len_URL)
        dis = len_cur - len_con
        if "http" not in j or j == URL or dis <= 3 or dis >= 15 or ori >= 20:
            continue
        if container in j:
            final.append(j)

    browser.close()
    return final


def load_model():
    with open('rf_classifier1', 'rb') as training_model:
        model = pickle.load(training_model)

    return model


def load_model2():
    with open('rf_classifier2', 'rb') as training_model:
        model = pickle.load(training_model)

    return model

URL = 'https://www.illinois.edu'
URL = 'https://www.berkeley.edu'
#URL = 'https://www.cornell.edu'
school = input("school:")
query = 'Computer Science Faculty'
result = give_input(URL,query)
gresult = google(school+query)

new_list = gresult.copy()

new_list.extend(x for x in result if x not in gresult)

final = []
for i in range(len(new_list)):
    temp = new_list[i].lower()
    if ('faculty' or 'people' or 'staff' or 'directory') in temp:
        final.append(new_list[i])

model = load_model()
final_web = ''
print(final)
for i in final:
    print(i)
    url = i
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    count_name_link = get_feature.get_name_feature(soup)
    count_professor = get_feature.get_professor_feature(soup)
    count_phone, count_email = get_feature.get_phone_email_feature(soup)
    count_image = get_feature.get_photo_feature(soup)
    if count_name_link >= 5:
        cn = 1
    else:
        cn = 0
    if count_professor >= 5:
        cp = 1
    else:
        cp = 0
    if count_phone >= 5:
        ch = 1
    else:
        ch = 0
    if count_email >= 5:
        ce = 1
    else:
        ce = 0
    if count_image >= 5:
        ci = 1
    else:
        ci = 0
    temp = [[cn,cp,ch,ce,ci]]
    print(temp)
    result = model.predict(temp)
    print(result)
    if result[0] == 1:
        final_web = i
        break

final2 = homepage_candidate = get_all(final_web,new_list)
count = int(input('Number of output:',))
model2 = load_model2()
final_3 = []
print(final2)
for i in final2:
    url = i
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    count_re = get_feature.get_reseach(soup)
    count_ri = get_feature.get_reseach_interest(soup)
    count_ra = get_feature.get_reseach_area(soup)
    count_ro = get_feature.get_reseach_overview(soup)
    count_b  = get_feature.get_biography(soup)
    count_sa = get_feature.get_selected_articles(soup)
    count_sp = get_feature.get_selected_publications(soup)
    count_ed = get_feature.get_education(soup)
    count_aw = get_feature.get_awards(soup)
    count_pr = get_feature.get_professor_feature(soup)
    count_phone, count_email = get_feature.get_phone_email_feature(soup)
    count_ts = get_feature.get_teaching(soup) + get_feature.get_student(soup)
    

    
    feature = []
    feature.append(count_re)
    feature.append(count_ri+count_ra+count_ro)

    feature.append(count_b)
    feature.append(count_sa + count_sp)

    feature.append(count_ed)
    feature.append(count_aw)
    feature.append(count_pr)
    feature.append(count_phone)
    feature.append(count_email)
    feature.append(count_ts)
    result = model2.predict([feature])
    print(feature)
    print(result)
    if result[0] == 1:
        final_3.append(i)
        count -= 1
    if count <= 0:
        break
    
    
model,vector = predict.load_model()
final_list = []
for url in final_3:
    temp = predict.predict(url, 'all', vector, model)
    final_list.append(temp)
for i in final_list:
    print(i)

    
    