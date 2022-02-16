

import numpy as np
import string
import re
import math
rpath = "../shakestxts/indextemps/"

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost',
                    username='moira',
                    password='rootlogin')
searchindb = client.searchin

uid2display = np.load(rpath+'uid2display.npy',allow_pickle='TRUE').item()
uid2tokens = np.load('./uid2tokens.npy',allow_pickle='TRUE').item()
term2index = np.load('./term2index.npy',allow_pickle='TRUE').item()
term2idf = np.load('./term2idf.npy',allow_pickle='TRUE').item()
uuid2newId = np.load('./changelineID.npy',allow_pickle='TRUE').item()

newInsertList = []
currentIdset = set()
for uid in uid2tokens.keys():
    tokenList = uid2tokens[uid]
    newId = uuid2newId[uid]
    if newId in currentIdset:
        continue
    currentIdset = currentIdset.union([newId])
    newInsert = dict()
    newInsert['_id'] = newId
    newInsert['tokenList'] = tokenList
    newInsertList.append(newInsert)

line2token = searchindb['line2token']
line2token.insert_many(newInsertList)

def changeentries(entries):
    newentries = []
    countset = set()
    for entry in entries.items():
        countset = countset.union([entry[1]])
    for count in countset:
        entryset = list()
        for entry in entries.items():
            newid = uuid2newId[entry[0]]
            if count == entry[1]:
                entryset.append([newid])
        newen = dict()
        newen['entrycount'] = count
        newen['entryset'] = entryset
        newentries.append(newen)
    return newentries, countset

index = 0
insertList = []
for newtoken in term2index.keys():
    thistoken = newtoken
    thisid = index
    newtokenidf = term2idf[newtoken]
    thisentries, countset = changeentries(term2index[newtoken])
    thisInfo = dict()
    thisInfo['_id'] = thisid
    thisInfo['tokenname'] = thistoken
    thisInfo['idf'] = newtokenidf
    thisInfo['entriesType'] = list(countset)
    thisInfo['entries'] = thisentries
    insertList.append(thisInfo)
    index += 1

token2info = searchindb['token2info']
token2info.insert_many(insertList)
