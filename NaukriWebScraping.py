#!/usr/bin/env python
# coding: utf-8

# ### Naukri Web Scraping Python Code
# ######   Shivani Anand

# In[1]:


pip install selenium pandas numpy requests webdriver-manager


# In[2]:


import io
import os
import requests
import selenium
import pandas as pd
import numpy as np
import time


# In[3]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[4]:


#Install driver
opts=webdriver.ChromeOptions()
opts.headless=False
driver = webdriver.Chrome(ChromeDriverManager().install() ,options=opts)
naukri = pd.DataFrame(columns=['Title', 'CompanyName','Salary','PostingDate','Location']) # creates master dataframe 

title_list = []
location_list = []
company_list = []
days_list = []
salary_list = []


for n in range(1,50):
 
    url='https://www.naukri.com/software-engineer-software-developer-data-analyst-data-scientist-machine-learning-engineer-hr-manager-project-manager-cloud-architect-full-stack-developer-full-stack-web-developer-big-data-consultant-jobs-'+str(n)+'?k=Software%20Engineer%2C%20Software%20Developer%2C%20Data%20Analyst%2C%20Data%20Scientist%2C%20Machine%20Learning%20Engineer%2C%20HR%20Manager%2C%20Project%20Manager%2C%20Cloud%20Architect%2C%20Full%20Stack%20Developer%2C%20Full%20Stack%20Web%20Developer%2C%20Big%20Data%20Consultant'
    driver.get(url)
    time.sleep(3)
    
    title = driver.find_elements(by=By.XPATH,value='//a[@class="title fw500 ellipsis"]')
    location=driver.find_elements(by=By.XPATH,value='//li[@class="fleft grey-text br2 placeHolderLi location"]')
    company=driver.find_elements(by=By.XPATH,value='//div[@class="mt-7 companyInfo subheading lh16"]')
    salary=driver.find_elements(by=By.XPATH,value='//li[@class="fleft grey-text br2 placeHolderLi salary"]')
    days=driver.find_elements(by=By.XPATH,value='//div[contains(@class,"type br2 fleft")]/span[@class="fleft fw500"]')

    #print(len(title) , len(location) , len(company) , len(salary) , len(days))
    for t in range(len(title)):
        title_list.append(title[t].text)
        location_list.append(location[t].text)
        company_list.append(company[t].text)
        salary_list.append(salary[t].text)
        days_list.append(days[t].text)
    
    
    
    
data_tuples = list(zip(title_list[1:],company_list[1:],salary_list[1:],days_list[1:],location_list[1:])) # list of each players name and salary paired together
temp_df = pd.DataFrame(data_tuples, columns=['Title', 'CompanyName','Salary','PostingDate','Location']) # creates dataframe of each tuple in list
naukri = naukri.append(temp_df) # appends to master dataframe        
driver.close()


# In[5]:


naukri.shape


# In[6]:


naukri.tail(100)


# In[7]:


naukri.isnull().sum()


# In[ ]:


naukri

