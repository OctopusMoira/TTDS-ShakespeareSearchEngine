# preprocessor getting ready
from nltk.stem.porter import PorterStemmer
import string
import numpy as np
import re
import math
import random
import phonetics
stemmer = PorterStemmer()

replacement = ""
for i in range(32):
    replacement += " "
stopwfile = open("./Ydata/stopw.txt")
stopw = []
for line in stopwfile.readlines():
    stopw.append(line.split("\n")[0])

wordlist = []
term2idf = np.load('./Ydata/regex/term2idf.npy',allow_pickle='TRUE').item()
for word in term2idf.keys():
    wordlist.append(word)
wordlist = " ".join(wordlist)

def query_tree(query, limit, andor, stem2idC, metadata, steminfo):
    resultList = []
    outputSize = limit
    uid2bm25 = dict()
    avgLen = metadata.find_one({'_id': 0})['avgLen']
    cleanedQ = []
    query = query.translate(str.maketrans(string.punctuation, replacement))
    withinSet = set()
    if andor == 1:
        for word in query.strip().split(" "):
            foldW = word.casefold()
            if foldW not in stopw:
                stemW = stemmer.stem(foldW)
                findMatch = stem2idC.find_one({'_id': stemW})
                if findMatch:
                    cleanedQ.append(findMatch['stemID'])
                    withinSet = withinSet.union(steminfo.find_one({'_id': findMatch['stemID']})['stemUIDC'].keys())
    elif andor == 0:
        first = 1
        for word in query.strip().split(" "):
            foldW = word.casefold()
            if foldW not in stopw:
                stemW = stemmer.stem(foldW)
                findMatch = stem2idC.find_one({'_id': stemW})
                if findMatch:
                    cleanedQ.append(findMatch['stemID'])
                    if first == 1:
                        withinSet = set(steminfo.find_one({'_id': findMatch['stemID']})['stemUIDC'].keys())
                        first = 0
                        continue
                    withinSet = withinSet.intersection(set(steminfo.find_one({'_id': findMatch['stemID']})['stemUIDC'].keys()))
    for uid in withinSet:
        bm25summ = 0
        fieldLen = len(cleanedQ)
        for termId in cleanedQ:
            findterm = steminfo.find_one({'_id': termId})
            finDt = 0
            if not findterm:
                continue
            if uid in findterm['stemUIDC'].keys():
                finDt = findterm['stemUIDC'][uid]
            bm25summ += ( findterm['stemIDF'] * (finDt * 2.2) / ( finDt + 1.2 * (0.25 + 0.75 * ( fieldLen / avgLen ))) ) # computation -> precomputed
        uid2bm25[uid] = bm25summ
    sortedResult = dict(sorted(uid2bm25.items(), key=lambda item: item[1], reverse=True))
    for uid in sortedResult.keys():
        outputSize -= 1
        resultList.append(uid)
        if outputSize <= 0:
            break
    return resultList

def retrieveDetails(uid_list, lineinfo):
    full_info = dict()
    resultlist = []
    for uid in uid_list:
        full_info_this = dict()
        full_info_this['uid'] = uid
        linfo = lineinfo.find_one({"_id": int(uid)})
        if len(linfo['detail']) == 5:
            full_info_this['code'] = linfo['detail']['code']
            full_info_this['actnum'] = linfo['detail']['actnum']
            full_info_this['scnum'] = linfo['detail']['scnum']
            full_info_this['lineRange'] = linfo['detail']['lineRange']
            full_info_this['speaker'] = linfo['detail']['speaker']
        else:
            full_info_this['code'] = linfo['detail']['code']
            full_info_this['actnum'] = ""
            full_info_this['scnum'] = ""
            full_info_this['lineRange'] = linfo['detail']['linenum']
            full_info_this['speaker'] = ""
        full_info_this['display'] = linfo['display']
        resultlist.append(full_info_this)
    full_info['result'] = resultlist
    return full_info

# expand the query
def expan_q(query):
    new_q = []
    for word in query.split():
        word = r'(\w*%s\w*)' % word
        expan_w = re.findall(word, wordlist)
        new_q += expan_w
    returnDict = dict()
    returnDict["result"] = []
    if new_q:
        returnDict["result"] = list(set(new_q))
    return returnDict

def weight_formula(term,docid):
    weight = 0
    if docid in term2index[term]:
        td = term2index[term][docid]
        weight = (1 + math.log(td,10)) * term2idf[term]
    return weight

def regGet(expanquery, limit, line2token, token2info): #
    uid2score = {}
    entryset = set()
    print(expanquery)
    for token in expanquery["result"]:
        tinfo = token2info.find_one({'tokenname': token})
        if tinfo:
            types = sorted(tinfo['entriesType'], reverse=True)
            countdown = limit * 100
            for type in types:
                for dics in tinfo['entries']:
                    if dics['entrycount'] == type:
                        for entry in dics['entryset']:
                            entryset = entryset.union(set(entry))
                            countdown -= 1
                            if countdown <= 0:
                                break
                        break
    for entry in entryset:
        sco = 0
        for token in expanquery["result"]:
            tinfo = token2info.find_one({'tokenname': token})
            td = 0
            for dics in tinfo['entries']:
                if entry in dics['entryset']:
                    td = dics['entrycount']
                    break
            if td == 0:
                continue
            weight = (1 + math.log(td,10)) * tinfo['idf']
            sco += weight
        uid2score[entry] = sco
    sortedResult = dict(sorted(uid2score.items(), key=lambda item: item[1], reverse=True))
    outputSize = limit
    resultList = []
    for uid in sortedResult.keys():
        outputSize -= 1
        resultList.append(uid)
        if outputSize < 0:
            break
    return resultList

def phoGet(word, phobox):
    word_pho = phonetics.metaphone(word)
    thispho = phobox.find_one({'sound': word_pho})
    returnDict = dict()
    if thispho:
        returnDict["result"] = thispho['tokenbox']
    return returnDict
