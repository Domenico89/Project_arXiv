#from  urllib.request import urlopen
#import shutil
import requests
import tempfile
import time
import pickle
import os

if not os.path.exists('./txt_db'): 
    print('Database not present, creating one.')
    os.makedirs('./txt_db')
    
timeout=10
already_have = set(os.listdir('./txt_db'))#getting list of papers that are already present in the directory  

num_to_add=0
num_added=0
with open('metadata_db','rb') as file:
    metadata_db=pickle.load(file)

for arXiv_id,metadata in metadata_db.items():
    pdf=arXiv_id+'.pdf'
    txt=arXiv_id+'.txt'
    #getting the link of the pdf from the metadata, this is positioned at the end of the list at position 'links'
    pdf_url=metadata['links'][-1]['href']+'.pdf'
    pdf_url=pdf_url.replace("arxiv.org", "export.arxiv.org")#changing the link to the link used for harvesting purposes
    txt_path='./txt_db/'+txt
    try:
        if not txt in already_have:
            num_to_add+=1
            with tempfile.NamedTemporaryFile() as tmp:
                r = requests.get(pdf_url)
                print('getting article %s' % (pdf_url))
                tmp.write(r.content)
                cmd = "pdftotext %s %s" % (tmp.name, txt_path)
                exit=os.system(cmd)
                if exit!=0:
                    print('it seems like there was an error in converting %s. Please try again later. Exit status %i'%(arXiv_id,exit))
                    #remove the article in case it was created
                    if os.path.isfile(txt_path):
                        os.system('rm '+txt_path)
                else: num_added+=1
            #req = urlopen(pdf_url, None, timeout)
            #with open(path, 'wb') as file:
            #   shutil.copyfileobj(req, file)
            #time.sleep(0.01)
        else:
            print('%s already exists, skipping' % (arXiv_id))
    
    except Exception as e:
        print('error downloading: ', pdf_url)
        print(e)
print('downloaded %i articles out of %i.'%(num_added,num_to_add))    
