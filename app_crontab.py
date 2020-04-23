import os
import pickle
from utils import Config, strip_extension
import numpy as np
from scipy import vstack

from celery import Celery
from celery.schedules import crontab
app = Celery('app_crontab', broker="pyamqp://guest@localhost//")
# disable UTC so that Celery can use local time
app.conf.enable_utc = False


@app.task
def new_articles():
    
    #Use the arXivAPI script to download the metadata of the newest articles
    os.remove('metadata_db')
    os.system('python3 arXivAPI.py --max_index=110')
    #Download articles into the local txt_db. Keeping them make it easier whenever we decide to train again tfidf
    os.system('python3 download_to_text.py') 
    
    with open('metadata_db', 'rb') as file:
        metadata_db = pickle.load(file)
    
    txts = os.listdir(Config.txt_db)

    #Remove old articles from the database
    for txt in txts:
        idx = strip_extension(txt)
        if idx not in metadata_db.keys():
            path = os.path.join(Config.txt_db,txt)
            os.remove(path)
        
    with open('vectorized_articles.p','rb') as file:
        vectorized_articles=pickle.load(file)
    
    txts = os.listdir(Config.txt_db)
    idxs = [strip_extension(txt) for txt in txts]
    #Position of papers that are already in the database
    pos = np.in1d(vectorized_articles['articles'],idxs).nonzero()[0]

    if len(pos)>0: 

        X_have = vectorized_articles['X'][pos]
        articles_have = vectorized_articles['articles'][pos]
        links_have = vectorized_articles['links'][pos]
        titles_have = vectorized_articles['titles'][pos]
    
        with open('tfidf.p','rb') as file:
            tfidf = pickle.load(file)    
    
        idxs_not_have = [idx for idx in idxs if idx not in set(vectorized_articles['articles'])]
        corpus = read_clean(idxs_not_have)
        X_not_have = tfidf.transform(corpus)
        titles_not_have = [metadata_db[article]['title'].replace('\n', '').replace('  ',' ') for article in idxs_not_have]
        links_not_have = [metadata_db[article]['links'][-1]['href'] for article in idxs_not_have]
    
     
        X = vstack([X_have,X_not_have])
        titles = np.concatenate((titles_have,titles_not_have))
        links = np.concatenate((links_have,links_not_have))
    
    
        dictionary = {'X':X,'articles':np.array(txt_labels_train),'links':np.array(articles),'titles':np.array(titles)}
        with open(Config.vectorized_articles,'wb') as file:
            pickle.dump(dictionary,file)    

# add "new_articles" to the beat schedule
app.conf.beat_schedule = {
    "new-articles-task": {
        "task": "app_crontab.new_articles",
        "schedule": crontab(minute="0",hour="5",day="6")
    }
}
