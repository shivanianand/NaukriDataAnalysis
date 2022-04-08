#!/usr/bin/env python
# coding: utf-8

# In[153]:


import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
from datetime import date,timedelta
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
import lxml
from datetime import date, timedelta


# In[154]:


title=[]
salary=[]
location=[]
company=[]
posting=[]
driver = webdriver.Chrome(ChromeDriverManager().install())


# In[155]:


current_date = date.today()
for x in range(2):
    url = "https://www.naukri.com/software-developer-software-engineer-graphic-designer-data-analyst-data-scientist-business-analyst-hr-manager-project-engineer-project-manager-qa-lead-jobs-"+str(x)+"?k=Software%20Developer%2C%20Software%20Engineer%2C%20Graphic%20Designer%2C%20Data%20Analyst%2C%20Data%20Scientist%2C%20Business%20Analyst%2C%20HR%20Manager%2C%20Project%20Engineer%2C%20Project%20Manager%2C%20QA%20Lead"
    driver.get(url)
    time.sleep(1)
    page = requests.get(URL)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find('div',class_='list')

    for a in results.find_all('article',class_='jobTuple bgWhite br4 mb-8'):
        Title=a.find('a', attrs={'class':'title fw500 ellipsis'})
        Salary=a.find('li', attrs={'class':'fleft grey-text br2 placeHolderLi salary'})
        Location=a.find('li', attrs={'class':'fleft grey-text br2 placeHolderLi location'})
        CompanyName=a.find('a',attrs={'class':'subTitle ellipsis fleft'})
        PostingDate=a.find('div', class_='jobTupleFooter mt-20')
        inDate = PostingDate.find_all('span',class_ = 'fleft fw500')
        #print(type(inDate))
        #print(inDate[-1].text)
            
        date = inDate[-1].text
        #calculating posting date
        date = date.split(' ')[0]
        date = re.sub("[^\d]", "", date)
        if date.isnumeric():
            date = int(date)
        else:
            date = 0
        date = current_date - timedelta(date)
    
        title.append(Title.text)
        salary.append(Salary.text)
        location.append(Location.text)
        company.append(CompanyName.text)
        posting.append(date)
        
driver.close()


# In[156]:


df = pd.DataFrame({"Title":title,"CompanyName":company,"Salary":salary,"PostingDate":posting,"Location":location})
df


# In[157]:


df.to_csv('withsoup.csv',index=False)


# In[ ]:




