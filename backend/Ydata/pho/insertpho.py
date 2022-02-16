import numpy as np
import string
import re
import phonetics

from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost',
                    username='moira',
                    password='rootlogin')

searchindb = client['searchin']

pho2term = np.load('./pho2term.npy',allow_pickle='TRUE').item()

insertlist = []
for key in pho2term.keys():
    if key != '':
        tokenbox = pho2term[key].split(" ")
        newinsert = dict()
        newinsert['sound'] = key
        newinsert['tokenbox'] = tokenbox
        insertlist.append(newinsert)

phoboxC = searchindb['phobox']
phoboxC.insert_many(insertlist)
