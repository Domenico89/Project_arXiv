"""
Script that train the model

"""
import pickle
import os
import numpy as np
import argparse
from random import shuffle

from utils import Config, strip_extension, read_clean, get_y

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score

import multiprocessing

n_jobs=multiprocessing.cpu_count()

parser = argparse.ArgumentParser()
parser.add_argument('--max_features',type=int,default=20000,help='max number of words learned by the model. Depending on the number of classes we need to classify it can be made smaller or bigger')
parser.add_argument('--max_train',type=int,default=10000,help='max number of papers to be used in the training of the tfidf')
parser.add_argument('--n_jobs',type=int,default=n_jobs,help='number of workers used in training the models')
parser.add_argument('--C',type=int,default=10,help='C value to use in the regualrization of the logistic regression')
args = parser.parse_args()


#Get the list of paper present in the database
txts = os.listdir(Config.txt_db)
idxs=[strip_extension(txt) for txt in txts]

tfidf = TfidfVectorizer(input='content',encoding='utf-8', decode_error='replace', 
             strip_accents='unicode',lowercase=True, analyzer='word', stop_words='english', 
             token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b', ngram_range=(1, 2),
             max_features = args.max_features, norm='l2', use_idf=True, smooth_idf=True, 
             sublinear_tf=True, max_df=1.0, min_df=8)

#hard copy of the list of papers
train_txt_paths = list(idxs) 
#shuffle the list of articles and crop it
shuffle(train_txt_paths) 
train_txt_paths = train_txt_paths[:min(len(train_txt_paths), args.max_train)]
#prepare the corpus
train_corpus = read_clean(train_txt_paths)
#fit the model
print('Training the TFIDF vectorizer.')
tfidf.fit(train_corpus)

if not os.path.exists(Config.model):
    os.makedirs(Config.model)

#save the tfid vectoriser
with open(Config.tfidf,'wb') as file:
    pickle.dump(tfidf,file)

print('Vectorizing the database. The result will be saved in %s .'%(Config.vectorized_articles))

#The database might contain more articles than the ones in metadata_db, which more strictly records the articles
#that we want to use for training

with open(Config.metadata_db,'rb') as file:
    metadata_db=pickle.load(file)
txt_labels_train=[]
for article in metadata_db.keys():
    article_path='txt_db/'+article+'.txt'
    if os.path.isfile(article_path):
        txt_labels_train.append(article)


corpus=read_clean(txt_labels_train)
X = tfidf.transform(corpus)

#save articles in vectorized form together with links and names
articles=[metadata_db[article]['links'][-1]['href'] for article in txt_labels_train]
dictionary={'X':X,'articles':np.array(txt_labels_train),'links':np.array(articles)}
with open(Config.vectorized_articles,'wb') as file:
    pickle.dump(dictionary,file)


#getting the labels
y=get_y(txt_labels_train)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

#train the logistic regression model
logr = LogisticRegression(n_jobs=args.n_jobs, C=args.C,solver='lbfgs',penalty='l2',multi_class='multinomial')
print('Training the logistic regression model.')
logr.fit(X_train, y_train)
y_pred = logr.predict(X_test)

print('Testing accuracy %s' % accuracy_score(y_test, y_pred))
print('Testing precision score: {}'.format(precision_score(y_test, y_pred, average='weighted')))

with open(Config.logr,'wb') as file:
    pickle.dump(logr,file)


