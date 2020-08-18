# импортируем pymongo
import pymongo
import gridfs
import json
import dns
from pymongo import MongoClient
from math import log

from bson.objectid import ObjectId
conn = MongoClient('')
db = conn.DB
coll = db.Image
fs = gridfs.GridFS(db)

def AddImage(str,image):
    array = json.loads(str)
    imageID = fs.put(image)
    meta = {'imageID': imageID, 'descriptor': array['descriptor'], 'meta': array['meta']}
    coll.insert_one(meta)

def FindImage(imageId):
    binar = ""
    flag = True
    image = coll.find_one({'_id': ObjectId(imageId)})
    id = image["imageID"]
    for i in db.fs.chunks.find({'files_id': id}, {'_id': 0, 'data': 1}):
        if(flag):
            binar += str(i['data'])
            flag = False
        else:
            binar[len(binar)-1] += str(i['data'])
    f = open("test1.jpg", "wb")
    f.write(binar.encode("utf-8"))
    f.close()

    return binar

def dist_bet_vec(fir_vec, sec_vec, n = 1000):
    dist = 0.0
    for i in range(n):
        dist += fir_vec[i] * log(fir_vec[i] / sec_vec[i])
    return dist

def search_image(desc):
    dist = []
    for men in coll.find():
        tmp_id = men["imageID"]
        tmp_desc = men["descriptor"]
        tmp_dist = dist_bet_vec(tmp_desc, desc, len(desc))
        dist.append((tmp_dist, tmp_id))
    dist.sort(key=lambda i: i[0])
    return dist[0: 10]

def FindImage_new(imageId):
    data = fs.get(ObjectId(imageId)).read()    
    return data

def FindMetaInfo(imageId):
    data = coll.find_one({'imageID': ObjectId(imageId)})
    return data["meta"]


