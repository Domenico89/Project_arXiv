# Project_arXiv
Project to help students and young researchers determine which category suits their articles and provide a set of articles that might be relevant to their work.

The scripts contained in this repository use pdftotext to transforms articles into strings. In Linux it can be installed with
sudo apt-get update && sudo apt-get install -y xpdf .

The web application contained in src/web_app can be found at www.arxiv-writer-support.com .

A video explaining the project can be found at www.loom.com/share/5e7b690643c24423958cadcabe5587f3 . 

## Folders and files in this repo

**[notebooks](./notebooks):**
- [Data_Harvesting.ipynb](./notebooks/Data_Harvesting.ipynb) illustrates how to use the arXiv API to get articles metadata and download them in txt form.
- [Training_Model.ipynb](./ntebooks/Training_Model.ipynb) describes how the model was trained using tfidf and logistic regression.
- [Recommender_Systems.ipynb](./notebooks/Recommender_Systems.ipynb) describes how we built the recommender system for the articles and a possible approach on how to evaluate it.

**[src](./src):**
- [arXivAPI.py](./src/arXivAPI.py) module that uses the arXiv API to download the articles metadata.
- [download_to_txt.py](./src/download_to_txt.py) download the articles and transforms into txt using pdftotxt.
- [training_model.py](./src/training_model.py) train the tfidf and the logistic regression.
- [utils.py](./src/utils.py) utility functions.

**[src/web_app](./src/web_app):**
- [app.py](./src/web_app/app.py) web application built with Flask.
- [config.py](./src/web_app/config.py) configuration file Flask.
- [app_crontab.py](./src/web_app/app_crontab.py) application that updates the database of papers every week by downloading the most recent articles from arXiv.
- [utils.py](./src/web_app/utils.py) utitlity functions.

**[src/web_app/templates](./src/web_app):** folder that contains the templates for the web application.
