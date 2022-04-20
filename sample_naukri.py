import apache_beam as beam
import argparse
from apache_beam.io.filesystems import FileSystems as beam_fs
from apache_beam.options.pipeline_options import PipelineOptions
#from apache_beam.testing.util import open_shards
from sys import argv
import re
import codecs
import csv
# from typing import Dict, Iterable, List
# from datetime import date,timedelta
# from datetime import date, timedelta

# import datetime
# import pickle

PROJECT_ID = "business-transformers"
SCHEMA = "Title:STRING, CompanyName:STRING, Experience:STRING, PostingDate:DATETIME, Location:STRING"
GOOGLE_APPLICATION_CREDENTIALS= r"C:\Users\ABC\Downloads\business-transformers-630800de2465.json"


def clean(data):
     # Title cleaning
    # data['Title'] = re.split('\(|-|:|I ',data['Title'])[0]
    if ("engineer" in data['Title'].lower()) and ("software" in data['Title'].lower()):
        data['Title']="Software Engineer"
    elif ("developer" in data['Title'].lower()) and ("software" in data['Title'].lower()):
        data['Title']="Software Developer"
    elif 'analyst' in data['Title'].lower():
        data['Title']="Data Analyst"
    elif 'scientist' in data['Title'].lower():
        data['Title']="Data Scientist"
    elif 'architect' in data['Title'].lower():
        data['Title']="Cloud Architect"
    elif ("project" in data['Title'].lower()) and ("manager" in data['Title'].lower()):
        data['Title']="Project Manager"
    elif (("hr" in data['Title'].lower()) or ("h r" in data['Title'].lower())) and ("manager" in data['Title'].lower()):
        data['Title']="HR Manager"
    elif (("ml" in data['Title'].lower()) or ("machine learning" in data['Title'].lower())) and ("engineer" in data['Title'].lower()):
        data['Title']="ML Engineer"
    elif ("big data" in data['Title'].lower()) and ("consultant" in data['Title'].lower()):
        data['Title']="Big Data Consultant"
    elif (("fullstack" in data['Title'].lower()) or ("full stack" in data['Title'].lower())) and ("developer" in data['Title'].lower()):
        data['Title']="Full Stack Developer"
    elif 'graphic' in data['Title'].lower():
        data['Title']="Graphic Designer"
    elif 'developer' in data['Title'].lower():
        data['Title']="Web Developer"
    elif 'consultant' in data['Title'].lower():
        data['Title']="Senior Consultant"
    elif 'writer' in data['Title'].lower():
        data['Title']="Technical Writer"
    else:
        data['Title']="others"

    # Location cleaning
    data['Location']=re.sub("\[|\]|'",'',data['Location'])
    if data['Location'].startswith('"'):
        data['Location']='Multi-location'
 
    # PostingDate Cleaning

    if len(data['PostingDate'])==2:
        data['PostingDate']=0
    else:
        num="".join(re.findall('\d', data['PostingDate']))
        if num.isdigit():
            data['PostingDate']=int(num)
        # data['PostingDate']=int("".join(re.findall('\d', data['PostingDate'])))
    import datetime
    data['PostingDate']=datetime.date.today()-datetime.timedelta(days=data['PostingDate'])

    # data=data.applyMap(lambda x: x.replace('\r\n',''))
    return data

def discard_incomplete(data):
    """Filters out records that don't have an information."""
    if (re.findall('[0-9]-[0-9][0-9] [a-z][a-z][a-z]', data['Experience'])) or (re.findall('[0-9]-[0-9] [a-z][a-z][a-z]', data['Experience'])) or (re.findall('[0-9] [a-z][a-z][a-z]', data['Experience'])):
        data['Experience']=data['Experience']
    else:
        data['Experience']=re.findall('[0-9]-[0-9][0-9] [a-z][a-z][a-z]', data['Experience'])
    # data['Experience']=re.findall('[0-9]-[0-9] [a-z][a-z][a-z]', data['Experience'])
    return len(data['Experience'])>0 and len(data['PostingDate'])>0


if __name__== '__main__':
    parser = argparse.ArgumentParser()
    known_args = parser.parse_known_args(argv)
     
    p = beam.Pipeline(options=PipelineOptions(temp_location="gs://c2cnaukaribucket/temp_local"))
    
    (p
    #  |'Read Data' >> beam.io.ReadFromText('gs://buc_har/naukri_local.csv', skip_header_lines=True)
     |'Read Data' >> beam.io.textio.ReadFromText("gs://c2cnaukaribucket/naukri_local1.csv",skip_header_lines = True)
    #  |'' >> beam.Map(lambda x: x.replace('\r\n',''))
     |'Split Data'>> beam.Map(lambda x: x.split(','))
     |'Convert Data To Dict' >> beam.Map(lambda x: {"Title": x[1], "CompanyName": x[2],"Experience":x[3], "PostingDate": x[4], "Location": x[5]})
     |'Discard Incomplete' >> beam.Filter(discard_incomplete)
     |'Clean Data' >> beam.Map(clean)
     
    #  |'print' >> beam.Map(print)
    #  |'Write to CSV' >> beam.io.WriteToText('gs://{0}/result_local/Output1'.format('buc_har'), file_name_suffix='.csv')
     |'Write to CSV' >> beam.io.WriteToText('gs://mabuck/Output',file_name_suffix='.csv')
    #  |'WriteToBigQuery' >> beam.io.WriteToBigQuery(
    #        '{0}:naukri_test.test_local1'.format(PROJECT_ID),
    #        schema=SCHEMA,
    #        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
    #        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
    #        )
     )
    p.run().wait_until_finish()