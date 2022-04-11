#!/usr/bin/env python
# coding: utf-8

# In[6]:


import time
import json
import pandas as pd
import re
import logging
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
opts=webdriver.ChromeOptions()
opts.headless=False
driver = webdriver.Chrome(ChromeDriverManager().install() ,options=opts)


def date_extract(jobs):
    filtered_data=[]  
    for value in jobs:
        if not value:
            filtered_data.append(str(date.today()))       
        else:
            for item in value: 
                integer_value=int(str(item))
                dt=date.today()-timedelta(integer_value)
                filtered_data.append(str(dt))
    return filtered_data  

def get_df_from_dict(jobs):
    df=pd.DataFrame.from_dict(jobs) #Creating DataFrame
    df.head(10)
    df=df.apply(lambda x: x.astype(str).str.lower()) #converting into lowercase to remove redundancy
    df.head()    
    #df.skills=[skill.split("\n") for skill in df.skills]
    df.location=[location.split(" ") for location in df.location]
    df=df.dropna()
    return df

def task_scrape():
    
    jobs={"title":[],
        "company":[],
        
        "experience":[],
        #"skills":[],
        "date":[],
        "scraper_run_dt_time":[],
        "location":[]
        #"jd_url":[]
        }
    final_df=pd.DataFrame(jobs)    
        #This outer loop is for number of pages to be scraped
        #for role in data["job_roles"]:
         #   jobs={key:[] for key in jobs}
            #print("hello",jobs)
    for n in range(1,4):
        driver.get('https://www.naukri.com/software-engineer-software-developer-data-analyst-data-scientist-machine-learning-engineer-hr-manager-project-manager-cloud-architect-full-stack-developer-full-stack-web-developer-big-data-consultant-jobs-'+str(n)+'?k=Software%20Engineer%2C%20Software%20Developer%2C%20Data%20Analyst%2C%20Data%20Scientist%2C%20Machine%20Learning%20Engineer%2C%20HR%20Manager%2C%20Project%20Manager%2C%20Cloud%20Architect%2C%20Full%20Stack%20Developer%2C%20Full%20Stack%20Web%20Developer%2C%20Big%20Data%20Consultant')
        time.sleep(4)
        job_container = driver.find_elements(By.CSS_SELECTOR,".jobTuple.bgWhite.br4.mb-8")
                # scraping the details from webpage
        for job in job_container:
            driver.implicitly_wait(20)
            title=job.find_element(By.CSS_SELECTOR,"a.title.fw500.ellipsis").text
            company=job.find_element(By.CSS_SELECTOR,"a.subTitle.ellipsis.fleft").text
            location=job.find_element(By.CSS_SELECTOR,".fleft.grey-text.br2.placeHolderLi.location").text
            try:
                exp=job.find_element(By.CSS_SELECTOR,".fleft.grey-text.br2.placeHolderLi.experience").text
            except Exception:
                exp="0 yrs"      
            #skills=job.find_element(By.CSS_SELECTOR,".tags.has-description").text
            date_string=job.find_element(By.CSS_SELECTOR,"[class^='type br2 fleft']").text  
                    # date_string contains strings like 2 day ago,just now,few hours ago                                                                                
            #jd=job.find_element(By.TAG_NAME,"a").get_attribute("href")
            date=re.findall(r'\d+',date_string) #extracting numbers out of the date_string
            jobs["title"].append(title)
            jobs["company"].append(company)
            jobs["location"].append(location)
            jobs["experience"].append(exp)
            #jobs["skills"].append(skills)
            jobs["date"].append(date)
            #jobs["jd_url"].append(jd)
            jobs["scraper_run_dt_time"].append(datetime.today())
    jobs["date"]=date_extract(jobs["date"])
    try:
        print(type(jobs))
        dataframe=get_df_from_dict(jobs)
        print(type(dataframe))
        dataframe[15:25]
        final_df=final_df.append(dataframe)
    except:
        logging.error("Error in dict_to_df")                
    now=datetime.today()
    dt_time=now.strftime("%H%M%S")
    dt=now.strftime("%Y%m%d")
    filename="scraped_"+dt+"_"+dt_time
    final_df.info()
    final_df[40:45]
    final_df.to_csv('{}.csv'.format(filename))
    driver.quit

task_scrape()


# In[ ]:




