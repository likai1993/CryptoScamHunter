#! /usr/bin/python3
from youtubesearchpython import VideosSearch
from youtubesearchpython import *
import pickle as pkl
from os import walk
import datetime, threading, time
from helper import YoutubeDislike

def get_likes_dislikes(videoId):
    url = "https://returnyoutubedislikeapi.com/Votes?videoId="
    with open("./results/likes_dislikes_results.txt", "a") as log:
        res = YoutubeDislike(url, videoId)
        log.write(res+"\n")
        log.flush()
        #print(res)
        time.sleep(1)

def get_info():
    f = []
    videoIds = []
    for (dirpath, dirnames, filenames) in walk("./results/rawVideos"):
        for f in filenames:
            if "videoInfo" in f:
                print(dirpath+"/"+f)
                myDicts = pkl.load(open(dirpath+"/"+f, "rb"))
                for item in myDicts:
                    #print(item['title'] + "\t" +item['id'])
                    #print(item['id'])
                    videoIds.append(item['id'])
    return videoIds

knownVideos=get_info()
for i in range(len(keywords)):
    t1 = threading.Thread(target=search_keyword, args=(i,))
    t1.start()
time.sleep(int(3600*24))
