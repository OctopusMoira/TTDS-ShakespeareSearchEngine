from pymongo import MongoClient
import numpy as np
import string

client = MongoClient()
client = MongoClient('localhost',
                    username='moira',
                    password='rootlogin')
rpath = "./shakestxts/indextemps/"
metadata = np.load(rpath+'metadata.npy',allow_pickle='TRUE').item()
stem2doc_count = np.load(rpath+'stem2doc_count.npy',allow_pickle='TRUE').item()
stem2uid_count = np.load(rpath+'stem2uid_count.npy',allow_pickle='TRUE').item()
uid2detail = np.load(rpath+'uid2detail.npy',allow_pickle='TRUE').item()
uid2display = np.load(rpath+'uid2display.npy',allow_pickle='TRUE').item()
stem2idf = np.load(rpath+'stem2idf.npy',allow_pickle='TRUE').item()
uid2stemlist = np.load(rpath+'uid2stemlist.npy',allow_pickle='TRUE').item()
code2title = np.load(rpath+'code2title.npy',allow_pickle='TRUE').item()
code2synopsis = np.load(rpath+'code2synopsis.npy',allow_pickle='TRUE').item()

searchdb = client['searchin']

metac = searchdb['metadata']
metac.insert_one({'_id': 0, 'avgLen': metadata['avgLen']})

steminfo = searchdb['steminfo']
stemset = set()
for key in stem2doc_count.keys():
    stemset = stemset.union([key])

uidset = set()
for key in uid2display.keys():
    uidset = uidset.union([key])
insertList = []
uidlist = list(uidset)

# mapping uid - index
uid2newindex = dict()
for index, uid in enumerate(uidlist):
    uid2newindex[uid] = index

def changeID(stemUIDC):
    newMap = dict()
    for uid in stemUIDC.keys():
        count = stemUIDC[uid]
        newMap[str(uid2newindex[uid])] = count
    sortednewMap = dict(sorted(newMap.items(), key=lambda item: item[1], reverse=True))
    topMap = dict()
    for item in sortednewMap.items():
        if item[1] <= 0:
            break
        topMap[item[0]] = item[1]
    return topMap

insertList = []
stemlist = list(stemset)
for index, stem in enumerate(stemlist):
    stemname = stem
    stemDocC = stem2doc_count[stem]
    stemIDF = stem2idf[stem]
    stemUIDC = stem2uid_count[stem]
    newinsert = dict()
    newinsert['_id'] = index
    newinsert['stemname'] = stemname
    newinsert['stemDocC'] = stemDocC
    newinsert['stemIDF'] = stemIDF
    newstemUIDC = changeID(stemUIDC)
    newinsert['stemUIDC'] = newstemUIDC
    insertList.append(newinsert)
steminfo.insert_many(insertList)

cat2codef = open('./shakestxts/category2code.txt', 'r')
code2gen = dict()
for line in cat2codef.readlines():
    cat, codes = line.split(":")
    print(cat.strip())
    for code in codes.split(","):
        code2gen[code.strip()] = cat.strip()
workinfo = searchdb['workinfo']
insertList = []
for code in code2title.keys():
    ccode = code
    ctitle = code2title[code]
    cgenre = code2gen[code]
    csynop = ""
    if code in code2synopsis.keys():
        csynop = code2synopsis[code]
    cinfo = dict()
    cinfo['_id'] = ccode
    cinfo['title'] = ctitle
    cinfo['genre'] = cgenre
    cinfo['synopsis'] = csynop
    insertList.append(cinfo)
workinfo.insert_many(insertList)

#uidset = set()
#for key in uid2display.keys():
#    uidset = uidset.union([key])
insertList = []
#uidlist = list(uidset)
for index, uid in enumerate(uidlist):
    uuid = uid
    udisplay = uid2display[uid]
    udetailraw = uid2detail[uid]
    udetail = dict()
    if len(udetailraw) == 5:
        udetail['code'] = udetailraw[0]
        udetail['actnum'] = udetailraw[1]
        udetail['scnum'] = udetailraw[2]
        udetail['speaker'] = udetailraw[3]
        udetail['lineRange'] = udetailraw[4]
    elif len(udetailraw) == 2:
        udetail['code'] = udetailraw[0]
        udetail['linenum'] = udetailraw[1]
    else:
        print(udetailraw)
        print("wrong detail with id: "+uid)
    thisline = dict()
    thisline['_id'] = index
#     thisline['uid'] = uuid
    thisline['display'] = udisplay
    thisline['detail'] = udetail
    insertList.append(thisline)
lineinfo = searchdb['lineinfo']
lineinfo.insert_many(insertList)

insertList = []
for index, stem in enumerate(stemlist):
    newinsert = dict()
    newinsert['_id'] = stem
    newinsert['stemID'] = index
    insertList.append(newinsert)
stem2idC = searchdb['stem2idC']
stem2idC.insert_many(insertList)

