import numpy as np

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
