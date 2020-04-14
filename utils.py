import numpy as np
import os
import re
import pickle

class Config(object):
    #path where to store model related stuff
    model='data'
    #path for metadata storing
    metadata_db=os.path.join(model,'metadata_db')
    #path for storing the articles in txt form
    txt_db=os.path.join(model,'txt_db')
    #folder where to store temporary pdfs
    tmp=os.path.join(model,'tmp') 
    #path for the vectorised articles
    vectorized_articles=os.path.join(model,'vectorized_articles.p')
    #paths of the trained models
    tfidf=os.path.join(model,'tfidf.p')
    logr=os.path.join(model,'logr.p')
    #paths for the citations
    citations_db=os.path.join(model,'citations_db')
    cited_vectorized=os.path.join(model,'cited_vectorized')
    citing_vectorized=os.path.join(model,'citing_vectorized')


def get_id_version(url):
    id_version=url[url.rfind('/')+1:].split('v')
    return id_version[0],int(id_version[1])

def strip_extension(name):
    return name[:name.rfind('.')]

def strip_extension_1(name):
    if type(name) is list or np.ndarray:
        return [x[:x.rfind('.')] if x.rfind('.')!=-1 else x for x in name]
    else:
        return name[:name.rfind('.')]

def read_clean(txts):
    for txt in txts:
        with open(os.path.join(Config.txt_db,txt+'.txt'),'r') as file:
            document=file.read()
            #remove the reference to the class that arxiv puts at the beginning of the papers
            document=re.sub('\[(.+?)\]','',document)
            #remove the reference to the paper that arxiv puts at the beginning of the papers
            document=re.sub('arXiv:(.*?) ','',document,1)
        yield document

def get_y(idxs):
    with open(Config.metadata_db,'rb') as file:
        metadata=pickle.load(file)
    return [metadata[idx]['arxiv_primary_category']['term'] for idx in idxs]
