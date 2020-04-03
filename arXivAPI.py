"""
Module that queries the arXiv API and download the metadata relative to the articles.

Part of this code comes from a readaptation of the brilliant work contained in
https://github.com/karpathy/arxiv-sanity-preserver.git

"""

import time
import pickle
import numpy as np
import urllib.request
import random
import feedparser
import argparse
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--search_cat',help='category used for the query used by arxiv API. See http://arxiv.org/help/api/user-manual#detailed_examples')
parser.add_argument('--start_index',type=int,default=0,help='0 = most recent API result')
parser.add_argument('--max_index',type=int,default=500,help='upper bound on paper index we will fetch for each category.')
parser.add_argument('--results_per_iteration',type=int,default=100,help='passed to arxiv API')
parser.add_argument('--wait_time',type=float,default=3.0,help='waiting time between iterationsto avoid being cut out by arXiv API')
args = parser.parse_args()


try:
    with open('metadata_db', 'rb') as file:
        metadata_db = pickle.load(file)
except Exception as e:
    print('error loading existing database: ',e)
    print('Starting from an empty one')
    metadata_db = {}

base_url='http://export.arxiv.org/api/query?'
    
if args.search_cat is None:
    with open('arXiv_categories','rb') as file:
    	arXiv_categories=(pickle.load(file)).values()
else:
    arXiv_categories=[args.search_cat]
        
    
num_added_tot=0

for cat in arXiv_categories:
    search_query='cat:'+cat
    
    num_cat_added_tot=0
    i=0
    while num_cat_added_tot<args.max_index:
        query = 'search_query=%s&sortBy=lastUpdatedDate&start=%i&max_results=%i' % (search_query,i, args.results_per_iteration)
   
        with urllib.request.urlopen(base_url+query) as url:
            response = url.read()
        parse = feedparser.parse(response)
        if len(parse.entries)==0:
            print('There are no more search results for category %s .'%(cat))
            break
            
        num_cat_added=0
        num_cat_old=0

        for e in parse.entries:
            idx,v=utils.get_id_version(e['id'])
            e['raw_id']=cat+'/'+idx
            e['version']=v
        #add the article to the database only if the article is not there already (keeping the version into consideration) 
        #and if the primary category of the search is the same as the one considered
            if e['arxiv_primary_category']['term']==cat and (not idx in metadata_db or v > metadata_db[idx]['version']):
                metadata_db[idx]=e
                num_cat_added+=1
                num_cat_added_tot+=1
            else:
                num_cat_old+=1
            if num_cat_added_tot>args.max_index-1:
                break
		    
        print('Added %i papers in category %s . Papers skipped %i'%(num_cat_added,cat,num_cat_old))
        i+=args.results_per_iteration
        num_added_tot=num_added_tot+num_cat_added
        
        #Waiting some seconds to avoid being cut out from arXiv
        time.sleep(args.wait_time+random.uniform(0,0.1))

        
print('Total number of papers added %i.'%(num_added_tot))

if num_added_tot > 0:
    with open('metadata_db', 'wb') as file:
        pickle.dump(metadata_db,file)
