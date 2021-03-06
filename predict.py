#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 23:49:35 2020

@author: guanhuali
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 23:46:46 2020

@author: guanhuali
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from data_process import get_connection, get_raw_data, data_process
import pickle
import re
import requests
from bs4 import BeautifulSoup
def load_model():
    with open('text_classifier', 'rb') as training_model:
        model = pickle.load(training_model)

    with open('vectorizer', 'rb') as vect:
        tfidf_vect = pickle.load(vect)
    return model, tfidf_vect


def predict(url, mode, vector, model):
    soup = get_connection(url)
    raw = get_raw_data(soup)
    data = data_process(raw, mode=mode)
    test_vec = vector.transform(data)
    prediction = model.predict(test_vec)
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
    # email = None
    # phone = None'
    
    page = requests.get(url)

    b_soup = BeautifulSoup(page.content, 'html.parser')


    phone = b_soup.find(string=phoneRegex)

    email = b_soup.find(string=emailRegex)
    
    # for j in data:
    #     ph = phoneRegex.search(j)
    #     mo = emailRegex.search(j)
    #     if ph != None:
    #         if len(ph.group()) >= 20:
    #             continue
    #         phone = ph.group()
    #     if mo != None:
    #         if len(mo.group()) >= 20:
    #             continue
    #         email = mo.group()
            
    #     if email != None and phone != None:
    #         break
    
    res = prediction.tolist()
    diction = {
        "url": url,
        "email": email,
        "phone": phone,
        "edu": [],
        "bio": [],
        "research": [],
        "award": []
        }

    for i in range(1, len(res) - 1):
        if res[i] == 0:
            if res[i - 1] == res[i + 1] and res[i - 1] in [1, 2, 3, 4]:
                res[i] = res[i - 1]
    for i in range(len(data)):
        if mode == 'edu':
            if res[i] == 1:
                print(data[i], '1')
        elif mode == 'bio':
            if res[i] == 2:
                print(data[i], '2')
        elif mode == 'research':
            if res[i] == 3:
                print(data[i], '3')
        elif mode == 'award':
            if res[i] == 4:
                print(data[i], '4')
        elif mode == 'all':
            if res[i] == 1:
                #print(data[i], '1')
                diction["edu"].append(data[i])
            if res[i] == 2:
                #print(data[i], '2')
                diction['bio'].append(data[i])
            if res[i] == 3:
                #print(data[i], '3')
                diction['research'].append(data[i])
            if res[i] == 4:
                #print(data[i], '4')
                diction['award'].append(data[i])
    return diction

# List of URL for testing prediction
test_list = ['https://cs.illinois.edu/about/people/all-faculty/yuanz']
#test_list = [
    # 'https://www.cs.princeton.edu/people/profile/dpd',
    # 'https://www.cs.princeton.edu/people/profile/rdondero',
    # 'https://www.cs.princeton.edu/people/profile/zdvir',
    # 'https://www.cs.princeton.edu/people/profile/bee',
    # 'https://www.cs.princeton.edu/people/profile/fellbaum',
    # 'https://www.cs.princeton.edu/people/profile/felten',
    # 'https://www.cs.princeton.edu/people/profile/af',
    # 'https://www.cs.princeton.edu/people/profile/rfish',
    # 'https://www.cs.princeton.edu/people/profile/mfreed',
    # 'https://www.cs.princeton.edu/people/profile/maia'
    # 'https://www.cc.gatech.edu/~dbatra/',  # Wrong
    # 'https://www.cc.gatech.edu/~umit/',  # Wrong
    # 'https://www.cc.gatech.edu/~chernova/',
    # 'https://www.cc.gatech.edu/~echow/',
    # 'https://www.cc.gatech.edu/~goodman/',  # Wrong
    # 'http://kinnisgosha.com/',
    # 'https://people.orie.cornell.edu/cleeyu/',
    # 'https://www.cs.cornell.edu/~hweather/research.php',
    # 'https://vansky.github.io/cv.html',
    # 'http://www.itrummer.org/',
    # 'http://www.cs.cornell.edu/info/people/tt/tim_teitelbaum.html',
    # 'https://tsg.ece.cornell.edu/people/g-edward-suh/',
    # 'https://people.ece.cornell.edu/wagner/',
    # 'http://www.cs.cornell.edu/~snavely/',  # Wrong
    # 'http://www.elaineshi.com/awards.html',
    # 'http://www.cs.cornell.edu/fbs/',
    # 'https://www.cs.cornell.edu/~asampson/research.html',
    # 'https://www.ece.cornell.edu/faculty-directory/kirstin-hagelskjaer-petersen',
    # 'http://tap2k.org/cv.html',
    # 'https://people.jacobs.cornell.edu/mor/#',

    # 'https://cs.illinois.edu/about/people/all-faculty/zaher',
    # 'https://cs.illinois.edu/about/people/all-faculty/sadve',
    # 'https://cs.illinois.edu/about/people/all-faculty/angrave',
    # 'https://cs.illinois.edu/about/people/all-faculty/mdbailey',
    # 'https://cs.illinois.edu/about/people/all-faculty/mattox',
    # 'https://cs.illinois.edu/about/people/all-faculty/nikita',
    # 'https://cs.illinois.edu/about/people/all-faculty/tbretl',
    # 'https://cs.illinois.edu/about/people/all-faculty/karthe', #
    # 'https://cs.illinois.edu/about/people/all-faculty/kcchang',
    # 'https://cs.illinois.edu/about/people/all-faculty/dchen',
    # 'https://cs.illinois.edu/about/people/all-faculty/girishc',
    # 'https://cs.illinois.edu/about/people/all-faculty/minhdo',
    # 'https://cs.illinois.edu/about/people/all-faculty/dullerud', #
    # 'https://cs.illinois.edu/about/people/all-faculty/melkebir',
    # 'https://cs.illinois.edu/about/people/all-faculty/jeffe',
    # 'https://cs.illinois.edu/about/people/all-faculty/waf',
    # 'https://cs.illinois.edu/about/people/all-faculty/jugal', #
    # 'https://cs.illinois.edu/about/people/all-faculty/pbg',
    # 'https://cs.illinois.edu/about/people/all-faculty/mgolpar', #
    # 'https://cs.illinois.edu/about/people/all-faculty/wgropp',
    # 'https://cs.illinois.edu/about/people/all-faculty/jhasegaw',
    # 'https://cs.illinois.edu/about/people/all-faculty/kkhauser',
    # 'https://cs.illinois.edu/about/people/all-faculty/heath',
    # 'https://cs.illinois.edu/about/people/all-faculty/dhoiem',
    # 'https://cs.illinois.edu/about/people/all-faculty/jianh',
    # 'https://cs.illinois.edu/about/people/all-faculty/w-hwu',
    # 'https://cs.illinois.edu/about/people/all-faculty/rkiyer',
    # 'https://cs.illinois.edu/about/people/all-faculty/hengji',
    # 'https://cs.illinois.edu/about/people/all-faculty/jiang56',

    # 'https://cs.illinois.edu/about/people/all-faculty/cwfletch',
    # 'https://cs.illinois.edu/about/people/all-faculty/miforbes',
    # 'https://cs.illinois.edu/about/people/all-faculty/daf',
    # 'https://cs.illinois.edu/about/people/all-faculty/friedman',
    # 'https://cs.illinois.edu/about/people/all-faculty/jugal',
    # 'https://cs.illinois.edu/about/people/all-faculty/c-gear',
    # 'https://cs.illinois.edu/about/people/all-faculty/ghose', #
    # 'https://cs.illinois.edu/about/people/all-faculty/girju',
    # 'https://cs.illinois.edu/about/people/all-faculty/pbg',
    # 'https://cs.illinois.edu/about/people/all-faculty/mgolpar'

    #
    # 'https://www.cs.utexas.edu/people/faculty-researchers/scott-aaronson',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/lorenzo-alvisi',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/joshua-baer',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/chandrajit-bajaj', #
    # 'https://www.cs.utexas.edu/people/faculty-researchers/dana-ballard',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/don-batory',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/angela-beasley',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/joydeep-biswas',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/robert-boyer', #
    # 'https://www.cs.utexas.edu/people/faculty-researchers/vijay-chidambaram',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/eunsol-choi',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/alan-cline',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/william-cook',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/inderjit-dhillon', #
    # 'https://www.cs.utexas.edu/people/faculty-researchers/isil-dillig',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/glenn-downing',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/greg-durrett',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/fares-fraij',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/anna-gal',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/mohamed-gouda', #
    # 'https://www.cs.utexas.edu/people/faculty-researchers/kristen-grauman', #
    # 'https://www.cs.utexas.edu/people/faculty-researchers/justin-hart',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/qixing-huang',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/akanksha-jain',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/chand-john',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/adam-klivans',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/philipp-kr%C3%A4henb%C3%BChl',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/simon-lam',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/calvin-lin',

    # 'https://www.cs.utexas.edu/people/faculty-researchers/yale-n-patt',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/andrew-whinston',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/david-zhigang-pan',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/karen-e-willcox',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/matthew-lease',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/rudolf-lioutikov',
    # 'https://www.cs.utexas.edu/people/faculty-researchers/j-tinsley-oden',

    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/abbeel.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/asanovic.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/ayazifar.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/bachrach.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/bajcsy.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/mball.html', #
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/dbamman.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/barsky.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/bartlett.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/bayen.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/blum.html', #
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/borgs.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/brewer.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/aydin.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/canny.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/jchayes.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/akcheung.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/alexch.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/clancy.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/colella.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/ncrooks.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/culler.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/darrell.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/demmel.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/denero.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/anca.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/prabal.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/efros.html', #
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/elghaoui.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hfarid.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/harrison.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hartmann.html', #
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/harvey.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hearst.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hellerstein.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hilfinger.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/joshhug.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/nilah.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/jiantao.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/jordan.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/joseph.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/kahan.html',

    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/kanazawa.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/karp.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/katz.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/klein.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/kubiatowicz.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/lee.html', #
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/svlevine.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/listgarten.html',
    # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/mlustig.html' #

#]

if __name__ == '__main__':
    model, vector = load_model()
    mode = input('Enter the mode:')
    for test in test_list:
        print(predict(test, mode,vector,model))
