import os
import utils

if not os.path.exists('txt_db'): 
    os.makedirs('txt_db')

already_have_txt = set(os.listdir('txt_db'))#getting list of papers that are already present in the directory  
pdfs = set(os.listdir('pdf_db'))


for pdf in pdfs:
    txt=strip_extension(pdf)+'.txt'
    
    if not txt in already_have_txt:
        pdf_path='./pdf_db/'+pdf
        txt_path='./txt_db/'+txt
        cmd = "pdftotext %s %s" % (pdf_path, txt_path)
        exit=os.system(cmd)
        #check that everything went well
        if exit!=0:
            print('it seems like there was an error in converting %s. Please try again later. Exit status %i'%(pdf_path,exit))
            #remove the article in case it was created
            if os.path.isfile(txt_path):
                os.system('rm '+txt_path)
