"""
Script that train the model

"""
import pickle
import os
import numpy as np
import utils
from random import shuffle

from utils import Config, strip_extension, read_clean, get_y

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score


#Get the list of paper present in the database
txts = os.listdir(Config.txt_db)
idxs=[strip_extension(txt) for txt in txts]

#max number of words learned by the model. Depending on the number of classes we need to classify it can be made smaller or bigger
max_features=20000

tfidf = TfidfVectorizer(input='content',encoding='utf-8', decode_error='replace', 
             strip_accents='unicode',lowercase=True, analyzer='word', stop_words='english', 
             token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b', ngram_range=(1, 2),
             max_features = max_features, norm='l2', use_idf=True, smooth_idf=True, 
             sublinear_tf=True, max_df=1.0, min_df=8)

#max number of papers to use in the training 
max_train=10000
#hard copy of the list of papers
train_txt_paths = list(idxs) 
#shuffle the list of articles and crop it
shuffle(train_txt_paths) 
train_txt_paths = train_txt_paths[:min(len(train_txt_paths), max_train)]
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
corpus=read_clean(idxs)
X = tfidf.transform(corpus)

#save articles in vectorized form
with open(Config.vectorized_articles,'wb') as file:
    pickle.dump(X,file)

#getting the labels
y=get_y(idxs)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

#train the logistic regression model
logr = LogisticRegression(n_jobs=4, C=10,solver='lbfgs',penalty='l2',multi_class='multinomial')
print('Training the logistic regression model.')
logr.fit(X_train, y_train)
y_pred = logr.predict(X_test)

print('Testing accuracy %s' % accuracy_score(y_test, y_pred))
print('Testing F1 score: {}'.format(f1_score(y_test, y_pred, average='weighted')))

with open(Config.logr,'wb') as file:
    pickle.dump(logr,file)


