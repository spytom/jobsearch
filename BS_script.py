

import pandas as pd
import sys
import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
import os
import gc

import requests
import time

from bs4 import BeautifulSoup
###################################################################################3
#set the general urls 
temp_list = []
section2=[
        '/de/stellenangebote/administration-hr-consulting-ceo/?page=',
        '/de/stellenangebote/banking-versicherungswesen/?page=',
        '/de/stellenangebote/bau-architektur-engineering/?page=',
        '/de/stellenangebote/bewachung-polizei-zoll-rettung/?page=',
        '/de/stellenangebote/chemie-pharma-biotechnologie/?page=',
        '/de/stellenangebote/einkauf-logistik-trading/?page=',
        '/de/stellenangebote/elektronik-technik-uhren/?page=',
        '/de/stellenangebote/fahrzeuge-handwerk-lager-transport/?page=',
        '/de/stellenangebote/finanzen-treuhand-immobilien/?page=',
        '/de/stellenangebote/gastronomie-lebensmittel-tourismus/?page=',
        '/de/stellenangebote/grafik-typografie-druck/?page=',
        '/de/stellenangebote/informatik-telekommunikation/?page=',
        '/de/stellenangebote/marketing-kommunikation-redaktion/?page=',
        '/de/stellenangebote/maschinen-anlagenbau-produktion/?page=',
        '/de/stellenangebote/medizin-pflege-therapie/?page=',
        '/de/stellenangebote/sport-wellness-kultur/?page=',
        '/de/stellenangebote/verkauf-kundendienst-innendienst/?page=',
        '/de/stellenangebote/verwaltung-bildung-soziales/?page=']

section=[
        'https://www.jobs.ch/de/stellenangebote/administration-hr-consulting-ceo/?region=',
        'https://www.jobs.ch/de/stellenangebote/banking-versicherungswesen/?region=',
        'https://www.jobs.ch/de/stellenangebote/bau-architektur-engineering/?region=',
        'https://www.jobs.ch/de/stellenangebote/bewachung-polizei-zoll-rettung/?region=',
        'https://www.jobs.ch/de/stellenangebote/chemie-pharma-biotechnologie/?region=',
        'https://www.jobs.ch/de/stellenangebote/einkauf-logistik-trading/?region=',
        'https://www.jobs.ch/de/stellenangebote/elektronik-technik-uhren/?region=',
        'https://www.jobs.ch/de/stellenangebote/fahrzeuge-handwerk-lager-transport/?region=',
        'https://www.jobs.ch/de/stellenangebote/finanzen-treuhand-immobilien/?region=',
        'https://www.jobs.ch/de/stellenangebote/gastronomie-lebensmittel-tourismus/?region=',
        'https://www.jobs.ch/de/stellenangebote/grafik-typografie-druck/?region=',
        'https://www.jobs.ch/de/stellenangebote/informatik-telekommunikation/?region=',
        'https://www.jobs.ch/de/stellenangebote/marketing-kommunikation-redaktion/?region=',
        'https://www.jobs.ch/de/stellenangebote/maschinen-anlagenbau-produktion/?region=',
        'https://www.jobs.ch/de/stellenangebote/medizin-pflege-therapie/?region=',
        'https://www.jobs.ch/de/stellenangebote/sport-wellness-kultur/?region=',
        'https://www.jobs.ch/de/stellenangebote/verkauf-kundendienst-innendienst/?region=',
        'https://www.jobs.ch/de/stellenangebote/verwaltung-bildung-soziales/?region=']

t1='a[href^="'
t2='"]'


region=['4','6','8','9','10','13','14','15','16',
        '17','18','19','20','21','22','23','24','25']

rr=len(region)-1

progress=1
for j in range(0,rr):
    for q in range(0,18):
        print(progress)
        print('-----')
        time.sleep(5.5) 
        page_url=section[q]
        url=page_url+region[j]
        page = requests.get(url)
        contents = page.content
        soup = BeautifulSoup(contents, 'html.parser')
        tt = []
    #need to extract the number of pages 
        z=t1+section2[q]+t2
        for ax in soup.select(z):
            tt.append(ax.get('href'))
        try:
            nr=str(tt[len(tt)-2])
            nx=int(nr.split('page=',1)[1].split('&reg')[0])
            nx=nx+1   
        except:
            nx=2
        for i in range(1,nx):
            k=str(i)
            print(i)
            url = page_url[:len(page_url)-7] +'page=' + k +'&'+ page_url[len(page_url)-7:]+region[j]
            page = requests.get(url)
            contents = page.content
            #extracts all the job urls 
            soup = BeautifulSoup(contents, 'html.parser')
            for ax in soup.select('a[href^="/de/stellenangebote/detail/"]'):
                       temp_list.append(ax.get('href'))
            progress=progress+1        
 
        
path="D:\Datasets\jobs.ch"
os.chdir(path)

ds=pd.DataFrame(temp_list)
ds.to_csv("job_url_march2018.csv")


##################################################################################3
#loop through individual jobs 
##################################################################################3
##################################################################################3

#
d = {'url': ['x'], 'jobtitle': ['x'],'company' : ['x'] ,'location' : ['x'] ,'firmtype' : ['x'],'jobtype' : ['x'], 'percent' : ['x'], 'level' : ['x']}
final = pd.DataFrame(data=d)


url='https://www.jobs.ch/de/stellenangebote/detail/8050763/?source=vacancy_search'

path="D:\Datasets\jobs.ch\html"
os.chdir(path)

nr_j=len(temp_list)-1

for i in range(0,nr_j):
    url='https://www.jobs.ch'+temp_list[i]
    page = requests.get(url)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')    
    #extract specific information
    #job title
    mydivs = soup.findAll("h1", {"class": "e-heading vacancy-ad-title h-base x--vacancy-title"})
    my=str(mydivs)
    m=my.split('<h1 class="e-heading vacancy-ad-title h-base x--vacancy-title">')
    jobtitle=m[1].split('</h1>')[0]
    #company 
    try:
        mydivs = soup.findAll("div", {"class": "vacancy-ad-company x--vacancy-ad-company"})
        my=str(mydivs)
        company=my.split('vacancy-ad-company x--vacancy-ad-company"><span>')[1].split('</span> — <span><span class="vacancy-ad-company-location">')[0]
        #location 
        loc=my.split('<span class="vacancy-ad-company-location">')[1].split('</span><span class="hidden-xs"> <span class="c-rating-stars"')[0]
    except:
        pass
    #type of employer
    try:
        mydivs = soup.findAll("div", {"class": "vacancy-ad-meta-info"})
        my=str(mydivs)
        firmtype=my.split('</span></li><li><span class="svg-icon icon icon-timer">')[0].split('</path></svg></span><span>')[1]
        jobtype=my.split('</span>,<!-- --> </span><span>')[0].split('</path></svg></span><span><span>')[1]
        percent=my.split('</span>,<!-- --> </span><span>')[1].split('</span></li><li><span class="svg-icon')[0]
        level=my.split('</span></li></ul></div></div></div>')[0].split('></path></svg></span><span>')[3]
    except:
        pass
    #add info to dataframe
    d = {'url': [url], 'jobtitle': [jobtitle],'company' : [company] ,'location' : [loc] ,'firmtype' : [firmtype],'jobtype' : [jobtype], 'percent' : [percent], 'level' : [level]}
    new=pd.DataFrame(data=d)
    final=final.append(new)
    jobtitle=""
    company=""
    loc=""
    firmtype=""
    jobtype=""
    percent=""
    level=""
    #save file as html
    xx='name_file_'+str(i)+'.html'
    file = open(xx, "wb")
    file.write(contents)
    file.close()

   
path="D:\Datasets\jobs.ch"
os.chdir(path)

final.to_csv("job_infos.csv")
