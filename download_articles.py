import os
import time
import pickle
import shutil
import random
from  urllib.request import urlopen
import utils

with open('metadata_db','rb') as file:
    metadata_db=pickle.load(file)

if not os.path.exists('pdf_db'): #create directory to store article if not present aready
    os.makedirs('pdf_db')

timeout=10 #waiting seconds before stopping the download
already_have = set(os.listdir('pdf_db')) #getting list of papers that are already present in the directory  

num_to_add=0
num_added=0
with open('metadata_db','rb') as file:
    metadata_db=pickle.load(file)

for arXiv_id,metadata in metadata_db.items():
    pdf=arXiv_id+'.pdf'
    #getting the link of the pdf from the metadata, this is positioned at the end of the list at position 'links'
    pdf_url=metadata['links'][-1]['href']+'.pdf'
    pdf_url=pdf_url.replace("arxiv.org", "export.arxiv.org")
    path='pdf_db/'+pdf
    try:
        if not pdf in already_have:
            num_to_add+=1
            req = urlopen(pdf_url, None, timeout)
            print('getting article %s' % (pdf_url))
            with open(path, 'wb') as file:
                shutil.copyfileobj(req, file)
            num_added+=1
            #time.sleep(0.05)
        else:
            print('%s already exists, skipping' % (path))
    
    except Exception as e:
        print('error incurred while downloading: ', pdf_url)
        print(e)
print('downloaded %i articles out of %i.'%(num_added,num_to_add))    
