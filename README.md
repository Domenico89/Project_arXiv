# Project_arXiv
Project to help students and young researchers determine which category suits their articles and provides a set of articles that might be relevant to their work.

The notebook Data_Harvesting.ipynb illustrate how to use the arXiv API to get articles metadata and download them in txt form, in Training_Model.ipynb we describe how the model was trained using tfidf and logistic regression. In Recommender_Systems.ipynb we describe how we built the recommender system for the articles and a possible approach on how to evaluate it.

In web_app we collect the web application developed with flask, that can be found at http://54.154.46.191/ .

The scripts conatined in this repository use pdftotext to transforms articles into strings. In linux it can be installed with
sudo apt-get update && sudo apt-get install -y xpdf .
