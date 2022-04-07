#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
from datetime import date,timedelta
from webdriver_manager.chrome import ChromeDriverManager


# In[6]:


title=[]
salary=[]
location=[]
company=[]
posting=[]
driver = webdriver.Chrome(ChromeDriverManager().install())

for x in range(500):
    url = "https://www.naukri.com/software-developer-software-engineer-graphic-designer-data-analyst-data-scientist-business-analyst-hr-manager-project-engineer-project-manager-qa-lead-jobs-"+str(x)+"?k=Software%20Developer%2C%20Software%20Engineer%2C%20Graphic%20Designer%2C%20Data%20Analyst%2C%20Data%20Scientist%2C%20Business%20Analyst%2C%20HR%20Manager%2C%20Project%20Engineer%2C%20Project%20Manager%2C%20QA%20Lead"
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    results = soup.find('div',class_='list')

    for a in results.find_all('article',class_='jobTuple bgWhite br4 mb-8'):
        Title=a.find('a', attrs={'class':'title fw500 ellipsis'})
        Salary=a.find('li', attrs={'class':'fleft grey-text br2 placeHolderLi salary'})
        Location=a.find('li', attrs={'class':'fleft grey-text br2 placeHolderLi location'})
        CompanyName=a.find('a',attrs={'class':'subTitle ellipsis fleft'})
        PostingDate=a.find('div', class_='jobTupleFooter mt-20')
    
        title.append(Title.text)
        salary.append(Salary.text)
        location.append(Location.text)
        company.append(CompanyName.text)
        posting.append(PostingDate.text)
driver.close()


# In[7]:


df = pd.DataFrame({"Title":title,"CompanyName":company,"Salary":salary,"PostingDate":posting,"Location":location})
df


# In[8]:


df.duplicated().sum()


# In[9]:


df.to_csv('naukri.csv',index=False)


# In[ ]:





# In[ ]:





# In[ ]:




