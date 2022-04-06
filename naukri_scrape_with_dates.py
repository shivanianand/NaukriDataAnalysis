#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import re
from datetime import date, timedelta
#from webdriver_manager.chrome import ChromeDriverManager
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


# In[ ]:


jobs={"roles":[],
     "companies":[],
     "locations":[],
     "Dates":[],
     "salary":[],
     }


# In[ ]:


MAX_PAGE_NUM = 5
MAX_PAGE_DIG = 3
driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
#driver = webdriver.Chrome(ChromeDriverManager().install())


# In[ ]:


for i in range(1, MAX_PAGE_NUM+1):
    page_num = (MAX_PAGE_DIG - len(str(i))) * "0" + str(i)
    #url="https://www.naukri.com/data-scientist-jobs-"+page_num+"?k=data%20scientist"
    url = "https://www.naukri.com/software-developer-software-engineer-graphic-designer-data-analyst-data-scientist-business-analyst-hr-manager-project-engineer-project-manager-qa-lead-jobs-"
    driver.get(url)
    time.sleep(1)
    lst=driver.find_elements_by_css_selector(".jobTuple.bgWhite.br4.mb-8")
    current_date = date.today()
    
    for job in lst:
    
        try:
            role=job.find_element_by_css_selector("a.title.fw500.ellipsis").text
            company=job.find_element_by_css_selector("a.subTitle.ellipsis.fleft").text
            location=job.find_element_by_css_selector(".fleft.grey-text.br2.placeHolderLi.location").text
            salaries=job.find_element_by_css_selector(".fleft.grey-text.br2.placeHolderLi.salary").text
            #date=job.find_element_by_css_selector(".type.br2.fleft.grey").text
            posting_date=job.find_elements_by_css_selector(".fleft.fw500")
            if type(posting_date) is not list:
                date = posting_date
            else:
                date = posting_date[-1].text
            #calculating posting date
            date = date.split(' ')[0]
            date = re.sub("[^\d]", "", date)
            if date.isnumeric():
                date = int(date)
            else:
                date = 0
            date = current_date - timedelta(date)
            
            
        except NoSuchElementException:
             pass
            
        
        jobs["roles"].append(role)
        jobs["companies"].append(company)
        jobs["locations"].append(location)
        jobs["salary"].append(salaries)
        jobs["Dates"].append(date)


# In[ ]:


df1=pd.DataFrame(jobs)
df1


# In[ ]:


df1.to_csv('naukri_final.csv',index=False)

