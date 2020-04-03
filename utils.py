import numpy as np
import os

class Config(object):
    #path for metadata storing
    metadata_db=os.path.join('data','metadata_db')
    #path for storing the articles in txt form
    txt_db=os.path.join('data','txt_db')
    #folder where to store temporary pdfs
    tmp=os.path.join('data','tmp') 


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
