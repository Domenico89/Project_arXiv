"""
Script that download the pdfs and produce the text files. The pdfs are removed to save space. 

Part of this code comes from a readaptation of the brilliant work contained in
https://github.com/karpathy/arxiv-sanity-preserver.git
"""

import os
import pickle
import shutil
from utils import Config
from  urllib.request import urlopen


with open(Config.metadata_db,'rb') as file:
    metadata_db=pickle.load(file)

if not os.path.exists(Config.tmp): #create directory to temporarily store pdfs if not present aready
    os.makedirs(Config.tmp)

if not os.path.exists(Config.txt_db): #create directory to temporarily store pdfs if not present aready
    os.makedirs(Config.txt_db)

timeout=10 #waiting seconds before stopping the download
already_have = set(os.listdir(Config.txt_db)) #getting list of papers that are already present in the directory  

num_to_add=0
num_added=0
with open(Config.metadata_db,'rb') as file:
    metadata_db=pickle.load(file)

for arXiv_id,metadata in metadata_db.items():
    pdf=arXiv_id+'.pdf'
    txt=arXiv_id+'.txt'
    #getting the link of the pdf from the metadata, this is positioned at the end of the list at position 'links'
    pdf_url=metadata['links'][-1]['href']+'.pdf'
    #make the link into the link specifically provided by arXiv for harvesting purposes 
    pdf_url=pdf_url.replace("arxiv.org", "export.arxiv.org")
    pdf_path=os.path.join(Config.tmp,pdf)
    txt_path=os.path.join(Config.txt_db,txt)
    try:
        if not txt in already_have:
            num_to_add+=1
            req = urlopen(pdf_url, None, timeout)
            print('Getting article %s' % (pdf_url))
            with open(pdf_path, 'wb') as file:
                shutil.copyfileobj(req, file)
            #converting the pdf into txt needs pdftotext on the system to run
            cmd = "pdftotext %s %s" % (pdf_path, txt_path)
            exit=os.system(cmd)
            #remove the pdf to save space
            os.system('rm %s'%(pdf_path))
            num_added+=1
            #check that everything went well
            if exit!=0:
                print('It seems like there was an error in converting %s. Please try again later. Exit status %i.'%(pdf,exit))
                #remove the article in case the file was created
                if os.path.isfile(txt_path):
                    os.system('rm '+txt_path)
                num_added-=1
            
        else:
            print('%s already exists, skipping.' % (arXiv_id))
    
    except Exception as e:
        print('An error incurred while downloading: %s .'%(pdf_url))
        print(e)
print('Downloaded %i articles out of %i.'%(num_added,num_to_add))    
