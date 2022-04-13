#!/usr/bin/env python
# coding: utf-8

# In[3]:


import time
import json
import pandas as pd
import re
import logging
import datetime
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
opts=webdriver.ChromeOptions()
opts.headless=False
driver = webdriver.Chrome(ChromeDriverManager().install() ,options=opts)


def dict_to_df(jobs):      
    df=pd.DataFrame.from_dict(jobs) #Creating DataFrame
    df.head(10)
    df=df.apply(lambda x: x.astype(str).str.lower()) #converting into lowercase to remove redundancy
    df.head()    
    df.skills=[skill.split("\n") for skill in df.skills]
    df.locations=[location.split(" ") for location in df.locations]
    df=df.dropna()
    return df


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



jobs={"roles":[],"companies":[],"locations":[],"experience":[],"skills":[],"dates":[]}   
final_df=pd.DataFrame(jobs)  
job_roles=["Software Engineer","Data Analyst","Web Developer","ML Engineer","Technical Writer","Senior Consultant","Project Manager"]
for role in job_roles:
    jobs={key:[] for key in jobs}
            
    for i in range(2,4):
        driver.get("https://www.naukri.com/{}-jobs-{}".format(role,i))
        time.sleep(4)
        job_container = driver.find_elements(By.CSS_SELECTOR,".jobTuple.bgWhite.br4.mb-8")
                
        for job in job_container:
            driver.implicitly_wait(20)
            role=job.find_element(By.CSS_SELECTOR,"a.title.fw500.ellipsis").text
            company=job.find_element(By.CSS_SELECTOR,"a.subTitle.ellipsis.fleft").text
            location=job.find_element(By.CSS_SELECTOR,".fleft.grey-text.br2.placeHolderLi.location").text
            try:
                exp=job.find_element(By.CSS_SELECTOR,".fleft.grey-text.br2.placeHolderLi.experience").text
            except Exception:
                exp="0 yrs"      
            skills=job.find_element(By.CSS_SELECTOR,".tags.has-description").text
            date_string=job.find_element(By.CSS_SELECTOR,"[class^='type br2 fleft']").text  
            jd=job.find_element(By.TAG_NAME,"a").get_attribute("href")
            date=re.findall(r'\d+',date_string) #extracting numbers out of the date_string
            jobs["roles"].append(role)
            jobs["companies"].append(company)
            jobs["locations"].append(location)
            jobs["experience"].append(exp)
            jobs["skills"].append(skills)
            jobs["dates"].append(date)
                    
        try:
            
            dataframe=dict_to_df(jobs)
            
            final_df=final_df.append(dataframe)
        except:
            logging.error("Error in dictictionary to dataframe conversion")                
        
print("Total Columns: ",final_df.shape[1],"Total Rows: ",final_df.shape[0])
       
final_df.to_csv('naukri_url.csv')
driver.quit

#task_scrape()


# In[6]:


#final_df.shape()


# In[ ]:




