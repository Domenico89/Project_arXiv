import os
import numpy as np
import pickle

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from config import Config
from model import model_load, get_class, from_pdf_to_vector, find_similar
import matplotlib.pyplot as plt

ALLOWED_EXTENSIONS = {'pdf'}

tfidf,logr=model_load('tfidf.p','logr.p')

with open('vectorized_articles.p','rb') as file:
    database=pickle.load(file)

app = Flask(__name__)
app.config.from_object(Config)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # clear the pdf folder 
            os.system('rm static/pdf/*')
            os.system('rm static/img/*')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pdf_path=os.path.join('static/pdf',filename)
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            flash('You are only allowed to upload pdf files')
            return redirect(request.url)
    return render_template("Starting_Page.html")

@app.route('/About')
def about():
    return render_template("About.html")

@app.route('/Terms')
def terms():
    return render_template("Terms.html")


@app.route('/analysis/<filename>',methods=['GET','POST'])
def uploaded_file(filename):
    img_name='static/img/'+filename+'.png'
    filename=os.path.join('static/pdf',filename)
    x,exit_status=from_pdf_to_vector(filename,tfidf)
    if exit_status!=0:
        flash('Sorry, it seems that something went wrong. Please try again.')
        return redirect('/')
    else:
        #Get the classes that best suit the article and the corresponding probabilities
        prob,clss=get_class(x,logr)
        #Find the first 10 similar articles to the one uploaded in the database
        similar_pos=find_similar(database['X'],x,9)[0]

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
 
        fig, ax = plt.subplots()
        ax.pie(prob, labels=clss, autopct='%1.1f%%', shadow=True, startangle=160,wedgeprops={"edgecolor":"0",'linewidth': 1})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        img_name='static/img/plot'+str(randint(0,500))+'.png'
        plt.savefig(img_name, bbox_inches = 'tight', pad_inches = 0)
       
        return render_template("classification.html",filename=os.path.join('/',filename),img=os.path.join('/',img_name),prob=prob,clss=clss,similar=database['links'][similar_pos])
    
if __name__ == '__main__':
    app.run()
