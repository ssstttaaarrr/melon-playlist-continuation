#!/usr/bin/env python
# coding: utf-8

# In[1]:


import copy
import math
import time
import random

import fire
import numpy as np
from scipy import sparse
from datetime import date

from arena_util import load_json
from arena_util import write_json

np.random.seed(525)


# In[2]:


testing = 1


# In[3]:


playlists_train = load_json('data/train.json')
playlists_valq = load_json('data/test.json')


# In[4]:


songs = load_json('data/song_meta.json')


# In[5]:


genres = load_json('data/genre_gn_all.json')


# In[6]:


playlists_train += playlists_valq


# In[7]:


playlists_test = load_json('data/val.json')
playlists_train += playlists_test


# In[8]:


"""발라드, 팝, 힙합, 인디, 락,
랩, 댄스, Pop, 재즈, 알앤비, OST, 피아노, 연주곡,
일렉, 클래식, 팝송, EDM, 아이돌, RnB, 일렉트로니카, 가요, 록, Jazz, 감성힙합, CCM, Rock, JPOP,
인디음악, HipHop, 트로트, electronica, 걸그룹,
bgm, 국내힙합, 드라마, 영화, 일렉트로닉, 외힙,
메탈, 밴드, 배경음악, 하우스, kpop,
외국힙합, 감성발라드, 국힙, 영화음악, 영화OST,
RNBSOUL, 팝송추천, 동요, 한국힙합,
드라마ost, 알엔비, 찬양, 피아노연주곡, 보이그룹,
쇼미더머니, 록메탈, 재즈추천, 남자아이돌, 케이팝,
해외힙합, 일본, 제이팝, Electronic, indie, ASMR
"""

tag_to_genre = {}

tag_to_genre['힙합'] = ['GN0300', 'GN1200']
tag_to_genre['락'] = ['GN0600', 'GN1000']
tag_to_genre['랩'] = ['GN0300', 'GN1200']
tag_to_genre['알앤비'] = ['GN0400', 'GN1300']
tag_to_genre['OST'] = ['GN1500']
tag_to_genre['피아노'] = ['GN1600', 'GN1800']
tag_to_genre['연주곡'] = ['GN1600', 'GN1800']
tag_to_genre['일렉'] = ['GN1100', 'GN2600', 'GN2700']
tag_to_genre['클래식'] = ['GN1600', 'GN1800']
tag_to_genre['EDM'] = ['GN1100', 'GN2600', 'GN2700']
tag_to_genre['RnB'] = ['GN0400', 'GN1300']
tag_to_genre['일렉트로니카'] = ['GN1100', 'GN2600', 'GN2700']
tag_to_genre['록'] = ['GN0600', 'GN1000']
tag_to_genre['감성힙합'] = ['GN0300', 'GN1200']
tag_to_genre['CCM'] = ['GN2100']
tag_to_genre['Rock'] = ['GN0600', 'GN1000']
tag_to_genre['JPOP'] = ['GN1900']
tag_to_genre['HipHip'] = ['GN0300', 'GN1200']
tag_to_genre['트로트'] = ['GN0700']
tag_to_genre['electronica'] = ['GN1100', 'GN2600', 'GN2700']
tag_to_genre['걸그룹'] = ['GN2500']
tag_to_genre['국내힙합'] = ['GN0300', 'GN1200']
tag_to_genre['드라마'] = ['GN1500']
tag_to_genre['영화'] = ['GN1500']
tag_to_genre['일렉트로닉'] = ['GN1100', 'GN2600', 'GN2700']
tag_to_genre['외힙'] = ['GN0300', 'GN1200']
tag_to_genre['메탈'] = ['GN0600', 'GN1000']
tag_to_genre['외국힙합'] = ['GN0300', 'GN1200']
tag_to_genre['감성발라드'] = ['GN0100']
tag_to_genre['국힙'] = ['GN0300', 'GN1200']
tag_to_genre['영화음악'] = ['GN1500']
tag_to_genre['영화OST'] = ['GN1500']
tag_to_genre['RNBSOUL'] = ['GN0400', 'GN1300']
tag_to_genre['팝송추천'] = ['GN0900', 'GN1900']
tag_to_genre['동요'] = ['GN2200']
tag_to_genre['한국힙합'] = ['GN0300', 'GN1200']
tag_to_genre['드라마ost'] = ['GN1500']
tag_to_genre['알엔비'] = ['GN0400', 'GN1300']
tag_to_genre['찬양'] = ['GN2100']
tag_to_genre['피아노연주곡'] = ['GN1600', 'GN1800']
tag_to_genre['보이그룹'] = ['GN2500']
tag_to_genre['쇼미더머니'] = ['GN0300', 'GN1200']
tag_to_genre['록메탈'] = ['GN0600', 'GN1000']
tag_to_genre['남자아이돌'] = ['GN2500']
tag_to_genre['해외힙합'] = ['GN0300', 'GN1200']
tag_to_genre['일본'] = ['GN1900']
tag_to_genre['제이팝'] = ['GN1900']
tag_to_genre['Electronic'] = ['GN1100', 'GN2600', 'GN2700']
tag_to_genre['ASMR'] = ['GN2800']


# In[9]:


"""2000년대, 90년대, 2010년대,
1990, 2000, 2019, 7080, 2010, 1980, 1990년대,
2017, 2020, 8090, 2018, 1970_80, 80년대, 
"""

tag_to_date = {}

tag_to_date['2000년대'] = (date(1995, 1, 1), date(2015, 1, 1))
tag_to_date['2000'] = (date(1995, 1, 1), date(2015, 1, 1))
tag_to_date['1990년대'] = (date(1985, 1, 1), date(2005, 1, 1))
tag_to_date['90년대'] = (date(1985, 1, 1), date(2005, 1, 1))
tag_to_date['1990'] = (date(1985, 1, 1), date(2005, 1, 1))
tag_to_date['2010년대'] = (date(2005, 1, 1), date(2025, 1, 1))
tag_to_date['2010'] = (date(2005, 1, 1), date(2025, 1, 1))
tag_to_date['2019'] = (date(2019, 1, 1), date(2020, 1, 1))
tag_to_date['7080'] = (date(1965, 1, 1), date(1995, 1, 1))
tag_to_date['1970_80'] = (date(1965, 1, 1), date(1995, 1, 1))
tag_to_date['1980'] = (date(1975, 1, 1), date(1995, 1, 1))
tag_to_date['2017'] = (date(2017, 1, 1), date(2018, 1, 1))
tag_to_date['2020'] = (date(2020, 1, 1), date(2021, 1, 1))
tag_to_date['8090'] = (date(1975, 1, 1), date(2005, 1, 1))
tag_to_date['2018'] = (date(2018, 1, 1), date(2019, 1, 1))
tag_to_date['80년대'] = (date(1975, 1, 1), date(1995, 1, 1))


# In[10]:


meaningless = {
    'R', '바','1','B','2','J','3','v','칠','앙','4','9','8','6','I','d','볾','7','w','H','왬'
,'m','5','0','푹','N','C','묩','켄','쎈','팎','ㄹ','으','웅','외','X','하','무','냥','U','A'
,'s','헿','웩','읭','능','윽','과','뀿','뀨','모','뫼','퇼','y','홓','혀','포','궁','55','56'
,'22','히힝','하핫','2부','40','78','2탄','50','18','8화','ㅎㅎ','4주','13','or','66','쿄쿄'
,'3년','뭐지','냠냠','한다','16','98','4화','2주','3초','않는','아녕','54','15','17','81','47'
,'3기','풬킨','2등','히힉','규규','않아','팊니','누뉴','77','팊콘','잉잉','1주','첫주','빠밤'
,'군머','5만','않고','7명','펌글','순실','퍽퍽','1탄','1년','우앵','노노','ww','예꾸'
,'이런','인듯','4슴','외츌','14','33','허허','6화','12','9화','3화','1화','5화','4시'
,'많다','그것','5초','ㅋㅋ','2화','1일','7화','30','05','06','07','매주','아아','00'
,'11','01','02','03','04','으악','우아','쟌디','2426','55','7연속','56','홓'
,'529곡','14회'
}


# In[11]:


start = time.time()

song_cnt = {}

for playlist in playlists_train:
    for sid in playlist['songs']:
        if sid not in song_cnt:
            song_cnt[sid] = 0
        song_cnt[sid] += 1
        
################################################################################################################################

adj = {}

for playlist in playlists_train:
    for sid1 in playlist['songs']:
        if sid1 not in adj:
            adj[sid1] = {}
        
        for sid2 in playlist['songs']:
            if sid1 == sid2:
                continue
            if sid2 not in adj[sid1]:
                adj[sid1][sid2] = 0
            adj[sid1][sid2] += 1
            
print(time.time() - start)


# In[12]:


start = time.time()

for sid1 in adj:
    '''
    s = 0
    for sid2 in adj[sid1]:
        s += adj[sid1][sid2]
    '''
    for sid2 in adj[sid1]:
        adj[sid1][sid2] /= song_cnt[sid1]
        #adj[sid1][sid2] /= s
        
print(time.time() - start)


# In[13]:


tag_cnt = {}

for playlist in playlists_train:
    for tag in playlist['tags']:
        if tag not in tag_cnt:
            tag_cnt[tag] = 0
        tag_cnt[tag] += 1

################################################################################################################################

adj_tag = {}

for playlist in playlists_train:
    for tag in playlist['tags']:
        if tag not in adj_tag:
            adj_tag[tag] = {}
        
        for sid in playlist['songs']:
            if sid not in adj_tag[tag]:
                adj_tag[tag][sid] = 0
            adj_tag[tag][sid] += 1

for tag in adj_tag:
    for sid in adj_tag[tag]:
        adj_tag[tag][sid] /= tag_cnt[tag]
            
################################################################################################################################

plist = {}

for i in range(len(playlists_train)):
    playlist = playlists_train[i]
    for sid in playlist['songs']:
        if sid not in plist:
            plist[sid] = {}
        plist[sid][i] = 1
        
################################################################################################################################
        
plist_tag = {}

for i in range(len(playlists_train)):
    playlist = playlists_train[i]
    for tag in playlist['tags']:
        if tag not in plist_tag:
            plist_tag[tag] = {}
        plist_tag[tag][i] = 1
        
################################################################################################################################
        
pop = {}

for playlist in playlists_train:
    for sid in playlist['songs']:
        if sid not in pop:
            pop[sid] = 0
        pop[sid] += 1
        
pop = sorted(pop.items(), key=lambda t : t[1], reverse=True)

################################################################################################################################

pop_genre = {}

for playlist in playlists_train:
    for sid in playlist['songs']:
        for gid in songs[sid]['song_gn_gnr_basket']:
            if gid not in pop_genre:
                pop_genre[gid] = {}
            if sid not in pop_genre[gid]:
                pop_genre[gid][sid] = 0
            pop_genre[gid][sid] += 1
            
for gid in pop_genre:
    pop_genre[gid] = sorted(pop_genre[gid].items(), key=lambda t : t[1], reverse=True)

################################################################################################################################

for indx in range(len(playlists_valq)):
    playlist = playlists_valq[indx]
    tmp = playlist['updt_date']
    
    year = int(tmp[0]) * 1000 + int(tmp[1]) * 100 + int(tmp[2]) * 10 + int(tmp[3])
    month = int(tmp[5]) * 10 + int(tmp[6])
    day = int(tmp[8]) * 10 + int(tmp[9])
    
    isValidDate = True
    try :
        date(year,month,day)
    except ValueError :
        isValidDate = False
        
    if not isValidDate:
        year = 1950
        month = 1
        day = 1
        
    playlist['updt_date'] = date(year, month, day)
    
for sid in range(len(songs)):
    tmp = songs[sid]['issue_date']
    
    year = int(tmp[0]) * 1000 + int(tmp[1]) * 100 + int(tmp[2]) * 10 + int(tmp[3])
    month = int(tmp[4]) * 10 + int(tmp[5])
    day = int(tmp[6]) * 10 + int(tmp[7])
    
    isValidDate = True
    try :
        date(year,month,day)
    except ValueError :
        isValidDate = False
        
    if not isValidDate:
        year = 1950
        month = 1
        day = 1
        
    songs[sid]['issue_date'] = date(year, month, day)
    
################################################################################################################################

adj_tag2 = {}
tags_cnt = {}

for playlist in playlists_train:
    for i in range(len(playlist['tags'])):
        for j in range(i + 1, len(playlist['tags'])):
            a = playlist['tags'][i]
            b = playlist['tags'][j]
            if a > b:
                a, b = b, a
            if (a, b) not in adj_tag2:
                adj_tag2[(a, b)] = {}
            if (a, b) not in tags_cnt:
                tags_cnt[(a, b)] = 0
            tags_cnt[(a, b)] += 1
            
            for sid in playlist['songs']:
                if sid not in adj_tag2[(a, b)]:
                    adj_tag2[(a, b)][sid] = 0
                adj_tag2[(a, b)][sid] += 1
                
for tags in adj_tag2:
    s = 0
    for sid in adj_tag2[tags]:
        s += adj_tag2[tags][sid]
    for sid in adj_tag2[tags]:
        #adj_tag2[tags][sid] /= s
        adj_tag2[tags][sid] /= tags_cnt[tags]


# In[14]:


""" utils
"""

standard = date(1900, 1, 1)

def possible(indx, sid):
    playlist = playlists_valq[indx]
    return songs[sid]['issue_date'] <= playlist['updt_date']

def tag_in_title(indx):
    playlist = playlists_valq[indx]
    title = playlist['plylst_title']
    title = title.replace(" ", "")
    
    ret = []
    L = len(title)
    for i in range(L):
        for j in range(i, L):
            s = title[i:j+1]
            
            if s not in tag_cnt:
                continue
            ret.append(s)
    return ret

def in_term(date, mean, var):
    width = 3
    return mean - width * np.sqrt(var) <= (date - standard).days and (date - standard).days <= mean + width * np.sqrt(var)

def in_range(pop_cnt, pop_mean, pop_var):
    width = 3
    return pop_mean - width * np.sqrt(pop_var) <= pop_cnt and pop_cnt <= pop_mean + width * np.sqrt(pop_var)

def allowed_genre(sid, appear):
    for gid in songs[sid]['song_gn_gnr_basket']:
        if gid in appear:
            return True
    return False

def allowed_term(sid, term):
    for d in term:
        if d[0] <= songs[sid]['issue_date'] and songs[sid]['issue_date'] <= d[1]:
            return True
    return False

def few_artist(indx):
    playlist = playlists_valq[indx]
    
    artist_score = {}
    tot = len(playlist['songs'])
    
    cnt = 0
    for sid in playlist['songs']:
        for aid in songs[sid]['artist_id_basket']:
            if aid not in artist_score:
                artist_score[aid] = 1
    
    return (tot != 0) and (len(artist_score) / tot < 0.4)
    
def few_album(indx):
    playlist = playlists_valq[indx]
    
    album_score = {}
    tot = len(playlist['songs'])
    
    for sid in playlist['songs']:
        aid = songs[sid]['album_id']
        if aid not in album_score:
            album_score[aid] = 1
        
    return (tot != 0) and (len(album_score) / tot < 0.4)

def is_our_artist(sid, artists):
    for aid in artists:
        if aid in songs[sid]['artist_id_basket']:
            return True
    return False

def is_our_album(sid, albums):
    return (songs[sid]['album_id'] in albums)

def max_artist(indx):
    playlist = playlists_valq[indx]
    
    artist = {}
    for sid in playlist['songs']:
        for aid in songs[sid]['artist_id_basket']:
            if aid not in artist:
                artist[aid] = 0
            artist[aid] += 1
            
    artist = sorted(artist.items(), key=lambda t : t[1], reverse=True)
    
    if len(artist) == 0:
        return 0, 0
    else:
        return artist[0][0], artist[0][1] / len(playlist['songs'])

def add(indx, ret, score):
    playlist = playlists_valq[indx]
    
    mean = 0
    var = 0
        
    if len(playlist['songs']) == 0:
        mean = 0
        var = 100000000000
    else:
        for sid in playlist['songs']:
            mean += (songs[sid]['issue_date'] - standard).days
        mean /= len(playlist['songs'])

        for sid in playlist['songs']:
            var += np.power((songs[sid]['issue_date'] - standard).days - mean, 2)
        var /= len(playlist['songs'])
        
    pop_mean = 0
    pop_var = 0
    
    if len(playlist['songs']) == 0:
        pop_mean = 0
        pop_var = 10000000000000
    else:
        for sid in playlist['songs']:
            pop_mean += song_cnt[sid]
        pop_mean /= len(playlist['songs'])
        
        for sid in playlist['songs']:
            pop_var += np.power(song_cnt[sid] - pop_mean, 2)
        pop_var /= len(playlist['songs'])
        
    ########################################################################################
    
    appear = []
    for tag in playlist['tags']:
        if tag in tag_to_genre:
            appear += tag_to_genre[tag]
            
    more_tag = tag_in_title(indx)
    for tag in more_tag:
        if tag in tag_to_genre:
            appear.append(tag)
            
    term = []
    for tag in playlist['tags']:
        if tag in tag_to_date:
            term.append(tag_to_date[tag])
            
    artists = {}
    for sid in playlist['songs']:
        for aid in songs[sid]['artist_id_basket']:
            if aid not in artists:
                artists[aid] = 0
            artists[aid] += 1
            
    albums = {}
    for sid in playlist['songs']:
        aid = songs[sid]['album_id']
        if aid not in albums:
            albums[aid] = 0
        albums[aid] += 1
            
    is_few_artist = few_artist(indx)
    is_few_album = few_album(indx)
    
    who, how = max_artist(indx)
    
    dom = 0
    if how > 0.75:
        dom = 1
    
    for key in score:
        if in_term(songs[key]['issue_date'], mean, var):
            score[key] *= 2
        
    for key in score:
        found = False
        for aid in songs[key]['artist_id_basket']:
            if aid in artists:
                found = True
                break
        if found:
            score[key] *= 1.5
            
    for key in score:
        for name in songs[key]['artist_name_basket']:
            if (name in playlist['tags']) or (name in more_tag):
                score[key] *= 1.5
                
    occur_genre = {}
    for sid in playlist['songs']:
        for gid in songs[sid]['song_gn_gnr_basket']:
            if gid not in occur_genre:
                occur_genre[gid] = 0
            occur_genre[gid] += 1
            
    for key in score:
        found = 0
        for gid in songs[key]['song_gn_gnr_basket']:
            if gid in occur_genre:
                found = 1
                break
        
        if found == 1:
            score[key] *= 1.2
            
    for key in score:
        found = 0
        for gid in songs[key]['song_gn_gnr_basket']:
            if gid in appear:
                found = 1
                break
        if found == 1:
            score[key] *= 1.5
    
        
    #######################################
    
    score = sorted(score.items(), key=lambda t : t[1], reverse=True)
        
    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or (not possible(indx, score[i][0])):
            continue
        if is_few_artist and (not is_our_artist(score[i][0], artists)):
            continue
        if is_few_album and (not is_our_album(score[i][0], albums)):
            continue
        if (dom == 1) and (who not in songs[score[i][0]]['artist_id_basket']):
            continue
        
        ret.append(score[i][0])
        
    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or (not possible(indx, score[i][0])):
            continue
        if (dom == 1) and (who not in songs[score[i][0]]['artist_id_basket']):
            continue
        
        ret.append(score[i][0])

def complete(indx, ret):
    playlist = playlists_valq[indx]
    
    mean = 0
    var = 0
        
    if len(playlist['songs']) == 0:
        mean = 0
        var = 1000000000
    else:
        for sid in playlist['songs']:
            mean += (songs[sid]['issue_date'] - standard).days
        mean /= len(playlist['songs'])

        for sid in playlist['songs']:
            var += np.power((songs[sid]['issue_date'] - standard).days - mean, 2)
        var /= len(playlist['songs'])
        
    pop_mean = 0
    pop_var = 0
    
    if len(playlist['songs']) == 0:
        pop_mean = 0
        pop_var = 10000000000000
    else:
        for sid in playlist['songs']:
            pop_mean += song_cnt[sid]
        pop_mean /= len(playlist['songs'])
        
        for sid in playlist['songs']:
            pop_var += np.power(song_cnt[sid] - pop_mean, 2)
        pop_var /= len(playlist['songs'])
        
    ########################################################################################
    
    appear = []
    for tag in playlist['tags']:
        if tag in tag_to_genre:
            appear += tag_to_genre[tag]
            
    more_tag = tag_in_title(indx)
    for tag in more_tag:
        if tag in tag_to_genre:
            appear.append(tag)
            
    term = []
    for tag in playlist['tags']:
        if tag in tag_to_date:
            term.append(tag_to_date[tag])
            
    artists = []
    for sid in playlist['songs']:
        for aid in songs[sid]['artist_id_basket']:
            artists.append(aid)
            
    albums = {}
    for sid in playlist['songs']:
        aid = songs[sid]['album_id']
        if aid not in albums:
            albums[aid] = 1
            
    is_few_artist = few_artist(indx)
    is_few_album = few_album(indx)
    
    who, how = max_artist(indx)
    
    dom = 0
    if how > 0.75:
        dom = 1
        
    ################ get max genre
        
    genre_score = {}
    tot = len(playlist['songs'])
    
    for sid in playlist['songs']:
        for gid in songs[sid]['song_gn_gnr_basket']:
            if gid not in genre_score:
                genre_score[gid] = 0
            genre_score[gid] += 1 / tot
            
    max_genre_score = 0
    max_genre = -1
    for key, value in genre_score.items():
        if max_genre_score < value:
            max_genre_score = value
            max_genre = key
        
    for i in range(len(pop)):
        if len(ret) == 100:
            break
        if (pop[i][0] in playlist['songs']) or (pop[i][0] in ret) or (not possible(indx, pop[i][0])):
            continue
        if not in_term(songs[pop[i][0]]['issue_date'], mean, var):
            continue
        if is_few_artist and (not is_our_artist(pop[i][0], artists)):
            continue
        if is_few_album and (not is_our_album(pop[i][0], albums)):
            continue
        if (dom == 1) and (who not in songs[pop[i][0]]['artist_id_basket']):
            continue
            
        ret.append(pop[i][0])
        
    for i in range(len(pop)):
        if len(ret) == 100:
            break
        if (pop[i][0] in playlist['songs']) or (pop[i][0] in ret) or (not possible(indx, pop[i][0])):
            continue
        if not in_term(songs[pop[i][0]]['issue_date'], mean, var):
            continue
        if (dom == 1) and (who not in songs[pop[i][0]]['artist_id_basket']):
            continue
            
        ret.append(pop[i][0])
        
    for i in range(len(pop)):
        if len(ret) == 100:
            break
        if (pop[i][0] in playlist['songs']) or (pop[i][0] in ret) or (not possible(indx, pop[i][0])):
            continue
        ret.append(pop[i][0])
        


# In[15]:


def solve_no_info(indx):
    ret = []
    
    more_tag = tag_in_title(indx)
    
    score = {}
    for mtag in more_tag:
        w = np.power(tag_cnt[mtag], 0.5)
        for key, val in adj_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w
            
    add(indx, ret, score)
    
    if len(ret) == 100:
        return ret
    
    complete(indx, ret)
    return ret

def solve_one_tag(indx):
    playlist = playlists_valq[indx]
    
    ret = []
    
    tag = playlist['tags'][0]
    
    score = {}
    for key, val in adj_tag[tag].items():
        score[key] = val
        
    add(indx, ret, score)
    
    if len(ret) == 100:
        return ret
    
    occur = {}
    for sid in ret:
        L = len(plist[sid])
        for key in plist[sid]:
            if key not in occur:
                occur[key] = 0
            occur[key] += 1 / math.log(7 + L, 8)
    
    score = {}
    for key, value in occur.items():
        p = playlists_train[key]
        w = np.power(value, 4)
        
        for sid in p['songs']:
            if sid not in score:
                score[sid] = 0
            score[sid] += w
            
    add(indx, ret, score)
    
    if len(ret) == 100:
        return ret
    
    more_tag = tag_in_title(indx)
    
    score = {}
    for mtag in more_tag:
        w = np.power(tag_cnt[mtag], 0.5)
        for key, val in adj_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w
            
    add(indx, ret, score)
    
    if len(ret) == 100:
        return ret
    
    complete(indx, ret)
    return ret

def solve_two_tag(indx):
    ret = []
    
    playlist = playlists_valq[indx]
    
    tag1 = playlist['tags'][0]
    tag2 = playlist['tags'][1]
    
    if tag1 > tag2:
        tag1, tag2 = tag2, tag1
    
    meaning = 30
    if tag_cnt[tag1] > meaning and tag_cnt[tag2] > meaning:
        w1 = np.power(tag_cnt[tag1], 0.125)
        w2 = np.power(tag_cnt[tag2], 0.125)
        
        intersection = {}
        for sid in adj_tag[tag1]:
            if sid in adj_tag[tag2]:
                intersection[sid] = adj_tag[tag1][sid] * w1 + adj_tag[tag2][sid] * w2
                
        add(indx, ret, intersection)
            
        if len(ret) == 100:
            return ret
    
    occur_tag = {}
    for tag in playlist['tags']:
        L = len(plist_tag[tag])

        for key in plist_tag[tag]:
            if key not in occur_tag:
                occur_tag[key] = 0
            occur_tag[key] += 1 / math.log(7 + L, 8)

    score = {}
    for key, value in occur_tag.items():
        p = playlists_train[key]
        w = np.power(value, 4)

        for sid in p['songs']:
            if sid not in score:
                score[sid] = 0
            score[sid] += w
    
    add(indx, ret, score)
    
    if len(ret) == 100:
        return ret
    
    more_tag = tag_in_title(indx)
    
    score = {}
    for mtag in more_tag:
        w = np.power(tag_cnt[mtag], 0.5)
        for key, val in adj_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w
            
    add(indx, ret, score)
    
    if len(ret) == 100:
        return ret
    
    complete(indx, ret)
    return ret

def solve_several_tag(indx):
    playlist = playlists_valq[indx]
    
    ret = []
    
    score = {}
    for i in range(len(playlist['tags'])):
        for j in range(i + 1, len(playlist['tags'])):
            tag1 = playlist['tags'][i]
            tag2 = playlist['tags'][j]
            
            if tag1 > tag2:
                tag1, tag2 = tag2, tag1
                
            if (tag1, tag2) not in adj_tag2:
                continue
                
            w = np.power(tags_cnt[(tag1, tag2)], 0.125)
            
            for sid in adj_tag2[(tag1, tag2)]:
                if sid not in score:
                    score[sid] = 0
                score[sid] += np.power(adj_tag2[(tag1, tag2)][sid], 0.125) * w
                
    score = sorted(score.items(), key=lambda t : t[1], reverse=True)

    for i in range(len(score)):
        if score[i][1] == 0:
            break
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or (not possible(indx, score[i][0])):
            continue
        ret.append(score[i][0])
        
    if len(ret) == 100:
        return ret
    
    score = {}
    occur_tag = {}
    for tag in playlist['tags']:
        L = len(plist_tag[tag])

        for key in plist_tag[tag]:
            if key not in occur_tag:
                occur_tag[key] = 0
            occur_tag[key] += 1 / math.log(7 + L, 8)

    for key, value in occur_tag.items():
        p = playlists_train[key]
        w = np.power(value, 4)

        for sid in p['songs']:
            if sid not in score:
                score[sid] = 0
            score[sid] += w
            
    score = sorted(score.items(), key=lambda t : t[1], reverse=True)

    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or (not possible(indx, score[i][0])):
            continue
        ret.append(score[i][0])
        
    if len(ret) == 100:
        return ret
    
    score = {}
    for tag in playlist['tags']:
        w = np.power(tag_cnt[tag], 0.125)
        for sid in adj_tag[tag]:
            if sid not in score:
                score[sid] = 0
            score[sid] += np.power(adj_tag[tag][sid], 0.125) * w
    score = sorted(score.items(), key=lambda t : t[1], reverse=True)

    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or (not possible(indx, score[i][0])):
            continue
        ret.append(score[i][0])
        
    if len(ret) == 100:
        return ret
        
    more_tag = tag_in_title(indx)
        
    score = {}
    for mtag in more_tag:
        w = np.power(tag_cnt[mtag], 0.5)
        for key, val in adj_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w
    score = sorted(score.items(), key=lambda t : t[1], reverse=True)
    
    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or (not possible(indx, score[i][0])):
            continue
        ret.append(score[i][0])
        
    for i in range(len(pop)):
        if len(ret) == 100:
            break
        if (pop[i][0] in playlist['songs']) or (pop[i][0] in ret) or (not possible(indx, pop[i][0])):
            continue
        ret.append(pop[i][0])
        
    
    return ret

def solve_only_tag(indx):
    playlist = playlists_valq[indx]
    
    if len(playlist['tags']) == 0:
        return solve_no_info(indx)
    elif len(playlist['tags']) == 1:
        return solve_one_tag(indx)
    elif len(playlist['tags']) == 2:
        return solve_two_tag(indx)
    else:
        return solve_several_tag(indx)

################################################################################################################################

def solve_main(indx):
    ret = []
    playlist = playlists_valq[indx]
    
    #######################################
    
    occur = {}
    for sid in playlist['songs']:
        if sid not in plist:
            continue
        
        L = len(plist[sid])
        for pid in plist[sid]:
            if pid not in occur:
                occur[pid] = 0
            occur[pid] += 1 / math.log(7 + L, 8)
            
    for tag in playlist['tags']:
        L = len(plist_tag[tag])
        
        for key in plist_tag[tag]:
            if key not in occur:
                #occur[key] = 0
                continue
            occur[key] += 1.2 * 1 / math.log(7 + L)
            
    more_tag = tag_in_title(indx)
    
    for tag in more_tag:
        L = len(plist_tag[tag])
        
        for key in plist_tag[tag]:
            if key not in occur:
                #occur[key] = 0
                continue
            occur[key] += 1.2 * 1 / math.log(7 + L)
    
    score = {}
    for key, val in occur.items():
        if val < 0.333:
            continue
        
        p = playlists_train[key]
        w = np.power(val, 4)
        
        for sid in p['songs']:
            if sid not in score:
                score[sid] = 0
            score[sid] += w
            
    score2 = {}
    for sid1 in playlist['songs']:
        for sid2, val in adj[sid1].items():
            w = np.power(1 + val, 0.5)
            
            if sid2 not in score:
                continue
            if sid2 not in score2:
                score2[sid2] = 0
            score2[sid2] += w
            
    for key in score:
        if key not in score2:
            continue
        score[key] *= np.power(score2[key], 0.25)
            
    add(indx, ret, score)
        
    if len(ret) == 100:
        return ret
    
    score = {}
    for sid1 in playlist['songs']:
        for sid2, val in adj[sid1].items():
            w = np.power(1 + val, 0.125)
            
            if sid2 not in score:
                score[sid2] = 0
            score[sid2] += w
            
    add(indx, ret, score)
    
    if len(ret) == 100:
        return ret
    
    complete(indx, ret)
    return ret

################################################################################################################################

def solve(indx):
    playlist = playlists_valq[indx]
    
    if len(playlist['songs']) == 0:
        return solve_only_tag(indx)
    elif len(playlist['tags']) == 0:
        return solve_only_song(indx)
    else:
        return solve_main(indx)
    
def test(indx):
    playlist = playlists_valq[indx]
    
    if len(playlist['songs']) == 0:
        return solve_only_tag(indx)
    #elif len(playlist['tags']) == 0:
    #    return []
    else:
        return solve_main(indx)


# In[16]:


rec_songs = {}

start = time.time()
timer = 0
for playlist in playlists_valq:
    if timer % 1000 == 0:
        print('timer:', timer, time.time() - start)
        start = time.time()
    
    pid = playlist['id']
    if testing == 1:
        rec_songs[pid] = test(timer)
    else:
        rec_songs[pid] = solve(timer)

    timer += 1


# In[17]:


############################ tag inference ################################


# In[18]:


###########################################################################


# In[19]:


adj_song_tag = {}
for playlist in playlists_train:
    for tag in playlist['tags']:
        for sid in playlist['songs']:
            if sid not in adj_song_tag:
                adj_song_tag[sid] = {}
            if tag not in adj_song_tag[sid]:
                adj_song_tag[sid][tag] = 0
            adj_song_tag[sid][tag] += 1
            
for u in adj_song_tag:
    sum_song_tag = 0
    
    for key in adj_song_tag[u]:
        sum_song_tag += adj_song_tag[u][key]
    for key in adj_song_tag[u]:
        adj_song_tag[u][key] /= sum_song_tag
            
##########################################################################################################################

adj_tag_tag = {}
for playlist in playlists_train:
    L = len(playlist['tags'])
    for tag1 in playlist['tags']:
        if tag1 not in adj_tag_tag:
            adj_tag_tag[tag1] = {}
        for tag2 in playlist['tags']:
            if tag1 == tag2:
                continue
            if tag2 not in adj_tag_tag[tag1]:
                adj_tag_tag[tag1][tag2] = 0
            adj_tag_tag[tag1][tag2] += 1
            
for u in adj_tag_tag:
    sum_tag_tag = 0
    
    for key in adj_tag_tag[u]:
        sum_tag_tag += adj_tag_tag[u][key]
    for key in adj_tag_tag[u]:
        adj_tag_tag[u][key] /= tag_cnt[u]
            
##########################################################################################################################

pop_tag = {}

for playlist in playlists_train:
    L = len(playlist['tags'])
    for tag in playlist['tags']:
        if tag not in pop_tag:
            pop_tag[tag] = 0
        pop_tag[tag] += 1
        
pop_tag = sorted(pop_tag.items(), key=lambda t : t[1], reverse=True)

##########################################################################################################################

pop_genre_tag = {}

for playlist in playlists_train:
    for tag in playlist['tags']:
        for sid in playlist['songs']:
            for gid in songs[sid]['song_gn_gnr_basket']:
                if gid not in pop_genre_tag:
                    pop_genre_tag[gid] = {}
                if tag not in pop_genre_tag[gid]:
                    pop_genre_tag[gid][tag] = 0
                pop_genre_tag[gid][tag] += 1
                
for gid in pop_genre_tag:
    pop_genre_tag[gid] = sorted(pop_genre_tag[gid].items(), key=lambda t : t[1], reverse=True)

##########################################################################################################################


##########################################################################################################################


# In[20]:


"""utils
"""

def add_tag(indx, ret, score):
    playlist = playlists_valq[indx]
    
    more_tag = tag_in_title(indx)
    
    for tag in more_tag:
        if tag in score:
            score[tag] *= 7
    
    score = sorted(score.items(), key=lambda t : t[1], reverse=True)
        
    for i in range(len(score)):
        if len(ret) == 10:
            break
        if (score[i][0] in playlist['tags']) or (score[i][0] in ret):
            continue
        
        ret.append(score[i][0])

def complete_tag(indx, ret):
    playlist = playlists_valq[indx]
    
    genre_score = {}
    tot = len(playlist['songs'])
    
    for sid in playlist['songs']:
        for gid in songs[sid]['song_gn_gnr_basket']:
            if gid not in genre_score:
                genre_score[gid] = 0
            genre_score[gid] += 1 / tot
            
    max_genre_score = 0
    max_genre = -1
    for key, value in genre_score.items():
        if max_genre_score < value:
            max_genre_score = value
            max_genre = key
    
    if max_genre in pop_genre_tag:
        for i in range(len(pop_genre_tag[max_genre])):
            if len(ret) == 10:
                break
            if (pop_genre_tag[max_genre][i][0] in playlist['tags']) or (pop_genre_tag[max_genre][i][0] in ret):
                continue

            ret.append(pop_genre_tag[max_genre][i][0])
    
    for i in range(len(pop_tag)):
        if len(ret) == 10:
            break
        if (pop_tag[i][0] in playlist['tags']) or (pop_tag[i][0] in ret):
            continue
            
        ret.append(pop_tag[i][0])


# In[21]:


def solve_tag_no_info(indx):
    ret = []
    
    more_tag = tag_in_title(indx)
    
    score = {}
    for mtag in more_tag:
        w = np.power(tag_cnt[mtag], 0.25)
        for key, val in adj_tag_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w
            
    add_tag(indx, ret, score)
    
    if len(ret) == 10:
        return ret
    
    complete_tag(indx, ret)
    return ret

def solve_tag_only_song(indx):
    ret = []
    
    playlist = playlists_valq[indx]
    
    occur = {}
    for sid in playlist['songs']:
        if sid not in plist:
            continue
        
        L = len(plist[sid])
        for pid in plist[sid]:
            if pid not in occur:
                occur[pid] = 0
            occur[pid] += 1 / math.log(7 + L, 8)
            
    more_tag = tag_in_title(indx)
    
    for tag in more_tag:
        L = len(plist_tag[tag])
        
        for key in plist_tag[tag]:
            if key not in occur:
                occur[key] = 0
            occur[key] += 0.5 * 1 / math.log(7 + L)
    
    score = {}
    for key, val in occur.items():
        #if val < 0.333:
        #    continue
        
        p = playlists_train[key]
        w = np.power(val, 4)
        
        for tag in p['tags']:
            if tag not in score:
                score[tag] = 0
            score[tag] += w
    
    add_tag(indx, ret, score)
    
    if len(ret) == 10:
        return ret
    
    more_tag = tag_in_title(indx)
    
    score = {}
    for mtag in more_tag:
        if mtag in meaningless:
            continue
        
        w = np.power(tag_cnt[mtag], 0.25)
        for key, val in adj_tag_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w
            
    add_tag(indx, ret, score)
    
    if len(ret) == 10:
        return ret
    
    complete_tag(indx, ret)
    return ret

def solve_tag_main(indx):
    ret = []
    
    playlist = playlists_valq[indx]
    
    score = {}
    for tag in playlist['tags']:
        if tag not in adj_tag_tag:
            continue
        
        for key, val in adj_tag_tag[tag].items():
            if val < 0.5:
                continue
            
            w = np.power(val, 0.125)
            
            if key not in score:
                score[key] = 0
            score[key] += w
            
    for sid in playlist['songs']:
        if sid not in adj_song_tag:
            continue
            
        for key, val in adj_song_tag[sid].items():
            w = np.power(val, 0.125)
            
            if key not in score:
                continue
            score[key] *= np.power(w, 0.01)
            
    add_tag(indx, ret, score)
    
    if len(ret) == 10:
        return ret
    
    occur = {}
    for sid in playlist['songs']:
        if sid not in plist:
            continue
        
        L = len(plist[sid])
        for pid in plist[sid]:
            if pid not in occur:
                occur[pid] = 0
            occur[pid] += 1 / math.log(7 + L, 8)
            
    for tag in playlist['tags']:
        L = len(plist_tag[tag])
        
        for key in plist_tag[tag]:
            if key not in occur:
                occur[key] = 0
            occur[key] += 4 * 1 / math.log(7 + L)
            
    more_tag = tag_in_title(indx)
    
    for tag in more_tag:
        L = len(plist_tag[tag])
        
        if tag in meaningless:
            continue
        
        for key in plist_tag[tag]:
            if key not in occur:
                occur[key] = 0
            occur[key] += 1 * 1 / math.log(7 + L)
    
    score = {}
    for key, val in occur.items():
        #if val < 0.333:
        #    continue
        
        p = playlists_train[key]
        w = np.power(val, 4)
        
        for tag in p['tags']:
            if tag not in score:
                score[tag] = 0
            score[tag] += w
    
    add_tag(indx, ret, score)
    
    if len(ret) == 10:
        return ret
    
    more_tag = tag_in_title(indx)
    
    score = {}
    for mtag in more_tag:
        if mtag in meaningless:
            continue
        
        w = np.power(tag_cnt[mtag], 0.5)
        for key, val in adj_tag_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w
            
    add_tag(indx, ret, score)
    
    if len(ret) == 10:
        return ret
    
    complete_tag(indx, ret)
    return ret

def solve_tag(indx):
    playlist = playlists_valq[indx]
    
    if len(playlist['songs']) == 0 and len(playlist['tags']) == 0:
        return solve_tag_no_info(indx)
    elif len(playlist['tags']) == 0:
        return solve_tag_only_song(indx)
    else:
        return solve_tag_main(indx)


# In[22]:


rec_tags = {}

timer = 0
for playlist in playlists_valq:
    if timer % 1000 == 0:
        print('timer:', timer)
    
    pid = playlist['id']
    rec_tags[pid] = solve_tag(timer)
    timer += 1


# In[23]:


answers = []

for playlist in playlists_valq:
    pid = playlist['id']
    answer = { 'id': pid, 'songs': rec_songs[pid], 'tags': rec_tags[pid] }
    answers.append(answer)


# In[24]:


write_json(answers, 'results.json')


# In[ ]:




