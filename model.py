import pickle
import os
import numpy as np
import re

def clean(article):
    document=re.sub('\[(.+?)\]','',article)
    document=re.sub(' [0-9]+ ','',document)
    document=re.sub('arxiv:(.*?) ','',document)
    yield document

def model_load(tfidf_path,model_path):
    with open(tfidf_path,'rb') as file:
        tfidf=pickle.load(file)
    with open(model_path,'rb') as file:
        model=pickle.load(file)
    return tfidf,model

def from_pdf_to_vector(pdf_path,tfidf):
    if not os.path.exists('./tmp'): 
        os.makedirs('./tmp')
    txt_path='./tmp/article.txt'
    cmd="pdftotext %s %s" % (pdf_path,txt_path)
    exit=os.system(cmd)
    with open(txt_path,'r') as file:
        article=file.read()
    x=tfidf.transform(clean(article))
    os.system("rm %s"%(txt_path))
    return x,exit

def find_similar(X,x,how_many):
    cos_similarity=X.dot(x.transpose())
    cos_similarity=np.asarray(cos_similarity.todense()).reshape(-1)
    return np.argsort(-cos_similarity)[:how_many+1]

def get_class(x,model): 
    prob=model.predict_proba(x)[0]
    pos=np.argsort(-prob)
    prob=np.dot(np.true_divide(prob[pos[:3]],np.sum(prob[pos[:3]])),100)
    prob=prob.astype(int)
    prob[1]=100-prob[2]-prob[0]
    return prob,model.classes_[pos[:3]]
