import numpy as np
import string
import re
import math

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost',
                    username='moira',
                    password='rootlogin')
searchindb = client.searchin

rpath = "../shakestxts/indextemps/"

uid2display = np.load(rpath+'uid2display.npy',allow_pickle='TRUE').item()
uid2tokens = np.load('./uid2tokens.npy',allow_pickle='TRUE').item()
term2index = np.load('./term2index.npy',allow_pickle='TRUE').item()
term2idf = np.load('./term2idf.npy',allow_pickle='TRUE').item()

searchindb.list_collection_names()

lineinfoC = searchindb.lineinfo

uuid2newId = dict()
for uid in uid2display.keys():
    thisline = lineinfoC.find_one({'display': uid2display[uid]})
    uuid2newId[uid] = thisline['_id']

len(uuid2newId)

np.save('./changelineID.npy', uuid2newId)


