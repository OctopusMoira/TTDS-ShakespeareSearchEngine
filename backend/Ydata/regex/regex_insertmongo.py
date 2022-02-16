from pymongo import MongoClient
import numpy as np

rpath = "../shakestxts/indextemps/"

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
    for entry in entries.items():
        newid = uuid2newId[entry[0]]
        count = entry[1]
        newen = dict()
        newen['entryid'] = newid
        newen['count'] = count
        newentries.append(newen)
    return newentries

index = 0
insertList = []
for newtoken in term2index.keys():
    thistoken = newtoken
    thisid = index
    newtokenidf = term2idf[newtoken]
    thisentries = changeentries(term2index[newtoken])
    thisInfo = dict()
    thisInfo['_id'] = thisid
    thisInfo['tokenname'] = thistoken
    thisInfo['idf'] = newtokenidf
    thisInfo['entries'] = thisentries
    insertList.append(thisInfo)
    index += 1

token2info = searchindb['token2info']
token2info.insert_many(insertList)
