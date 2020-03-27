def get_id_version(url):
    id_version=url[url.rfind('/')+1:].split('v')
    return id_version[0],int(id_version[1])

def strip_extension(name):
    return name[:name.rfind('.')]
