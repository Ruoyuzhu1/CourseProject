#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 16:58:43 2020

@author: guanhuali
"""


from bs4 import BeautifulSoup
import requests
import re
from collections import Counter

def get_name_feature(soup):
    result = []
    for tag in soup.find_all('a'):
        if tag.has_attr('href'):
            temp = tag.get('href')
            if len(temp) <= 1:
                continue
            if temp[-1] == "/":
                temp = temp[0:-1]
            for i in range(len(temp)):
                if temp[-i-1] == "/":
                    temp = temp[0:-i-1]
                    break
            result.append(temp)
    count = Counter(result)
    #print(count.most_common(1)[0][1])
    return count.most_common(1)[0][1]

def get_professor_feature(soup):
    reg = re.compile(r'''((.*)[Pp]rofessor(.*))''', re.VERBOSE)
    count = 0
    for i in soup.find_all(string = reg):
        count += 1
    return count

def get_phone_email_feature(soup):
#email and phone count

    import re

    phoneRegex = re.compile(r'''(
        (.*)
        (\d{3}|\(\d{3}\))?              # area code
        (\s|-|\.)?                      # separator
        (\d{3})                         # first 3 digits
        (\s|-|\.)                       # separator
        (\d{4})                         # last 4 digits
        (\s*(ext|x|ext\.)\s*(\d{2,5}))? # extension
        (.*)
        )''', re.VERBOSE)

    emailRegex = re.compile(r'''(
        (.*)
        [a-zA-Z0-9._%+-]+
        @
        [a-zA-Z0-9.-]+
        (.*)
    )''', re.VERBOSE)

    matchesphone = 0


    matchesemail = 0

    for p in soup.find_all('a',href=phoneRegex):
        matchesphone += 1
    for e in soup.find_all('a',href=emailRegex):
        matchesemail += 1  
    for p in soup.find_all(string=phoneRegex):
        matchesphone += 1
    for e in soup.find_all(string=emailRegex):
        matchesemail += 1


    return matchesphone,matchesemail

#photo count
def get_photo_feature(soup):
    countimage = 0

    for p in soup.find_all('img'):
        countimage += 1
    for e in soup.find_all('div',{"class": "photo"}):
        countimage += 1
    return countimage


def get_reseach(soup):
    searched_word = 'Research'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)

    return len(results)

def get_reseach_interest(soup):
    searched_word = 'Research Interest'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)

    return len(results)

def get_reseach_area(soup):
    searched_word = 'Research Area'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)

    return len(results)

def get_reseach_overview(soup):
    searched_word = 'Research Overview'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)

    return len(results)

def get_biography(soup):
    searched_word = 'Biography'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)

    return len(results)

def get_selected_articles(soup):
    searched_word = 'Selected Articles'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)

    return len(results)

def get_selected_publications(soup):
    searched_word = 'Selected Publication'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)

    return len(results)

def get_education(soup):
    searched_word = 'Education'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)

    return len(results)

def get_awards(soup):
    searched_word = 'Awards'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
    return len(results)

def get_teaching(soup):
    searched_word = 'teaching'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
    return len(results)


def get_student(soup):
    searched_word = 'student'
    results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
    return len(results)
