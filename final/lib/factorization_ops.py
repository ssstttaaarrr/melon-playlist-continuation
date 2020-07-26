# from lib.data.data_loader import *
from tqdm import tqdm

# # Song matrix
# song_cnt = {}
# tag_cnt = {}
# tags_cnt = {}
# adj_song = {}
# adj_tag = {}
# plist = {}
# plist_tag = {}
# adj_tag2 = {}
# pop = {}
# pop_genre = {}
#
# # Tag matrix
# adj_song_tag = {}
# adj_tag_tag = {}
# pop_tag = {}
# pop_genre_tag = {}
#
# songs = None

# def load_train_data(train_play_list, songs_meta):
#     global playlists_train
#     global songs
#
#     playlists_train = train_play_list
#     songs = songs_meta

def build_song_cnt(playlists_train):
    song_cnt = {}
    for playlist in playlists_train:
        for sid in playlist['songs']:
            if sid not in song_cnt:
                song_cnt[sid] = 0
            song_cnt[sid] += 1

    return song_cnt


def build_adj_song(playlists_train, song_cnt):
    adj_song = {}
    for playlist in tqdm(playlists_train):
        for sid1 in playlist['songs']:
            if sid1 not in adj_song:
                adj_song[sid1] = {}

            for sid2 in playlist['songs']:
                if sid1 == sid2:
                    continue
                if sid2 not in adj_song[sid1]:
                    adj_song[sid1][sid2] = 0
                adj_song[sid1][sid2] += 1

    for sid1 in adj_song:
        '''
        s = 0
        for sid2 in adj[sid1]:
            s += adj[sid1][sid2]
        '''
        for sid2 in adj_song[sid1]:
            adj_song[sid1][sid2] /= song_cnt[sid1]
            # adj[sid1][sid2] /= s

    return adj_song


def build_tag_cnt(playlists_train):
    tag_cnt = {}
    for playlist in playlists_train:
        for tag in playlist['tags']:
            if tag not in tag_cnt:
                tag_cnt[tag] = 0
            tag_cnt[tag] += 1

    return tag_cnt

def build_adj_tag(playlists_train, tag_cnt):
    adj_tag = {}
    for playlist in tqdm(playlists_train):
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

    return adj_tag

def build_plist(playlists_train):
    plist = {}
    for i in range(len(playlists_train)):
        playlist = playlists_train[i]
        for sid in playlist['songs']:
            if sid not in plist:
                plist[sid] = {}
            plist[sid][i] = 1

    return plist


def build_plist_tag(playlists_train):
    plist_tag = {}
    for i in range(len(playlists_train)):
        playlist = playlists_train[i]
        for tag in playlist['tags']:
            if tag not in plist_tag:
                plist_tag[tag] = {}
            plist_tag[tag][i] = 1

    return plist_tag


def build_pop(playlists_train):
    pop = {}
    for playlist in playlists_train:
        for sid in playlist['songs']:
            if sid not in pop:
                pop[sid] = 0
            pop[sid] += 1
    pop = sorted(pop.items(), key=lambda t: t[1], reverse=True)

    return pop


def build_pop_genre(playlists_train, songs):
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
        pop_genre[gid] = sorted(pop_genre[gid].items(), key=lambda t: t[1], reverse=True)

    return pop_genre


def build_adj_tag2(playlists_train):
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
            # adj_tag2[tags][sid] /= s
            adj_tag2[tags][sid] /= tags_cnt[tags]

    return adj_tag2, tags_cnt



################################################################ TAG factorization

def build_tags_cnt(data_loader, factorizer):
    tags_cnt = {}
    print('[ADJ_TAG2]')
    for playlist in tqdm(data_loader.playlists_train):
        for i in range(len(playlist['tags'])):
            for j in range(i + 1, len(playlist['tags'])):
                a = playlist['tags'][i]
                b = playlist['tags'][j]
                if a > b:
                    a, b = b, a
                if (a, b) not in factorizer.adj_tag2:
                    factorizer.adj_tag2[(a, b)] = {}
                if (a, b) not in tags_cnt:
                    tags_cnt[(a, b)] = 0
                tags_cnt[(a, b)] += 1

                for sid in playlist['songs']:
                    if sid not in factorizer.adj_tag2[(a, b)]:
                        factorizer.adj_tag2[(a, b)][sid] = 0
                        factorizer.adj_tag2[(a, b)][sid] += 1

    print('[ADJ_TAG2]')
    for tags in tqdm(factorizer.adj_tag2):
        s = 0
        for sid in factorizer.adj_tag2[tags]:
            s += factorizer.adj_tag2[tags][sid]
        for sid in factorizer.adj_tag2[tags]:
            #adj_tag2[tags][sid] /= s
            factorizer.adj_tag2[tags][sid] /= tags_cnt[tags]

    return tags_cnt


def build_adj_song_tag(playlists_train):
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

    return adj_song_tag
##########################################################################################################################


def build_adj_tag_tag(playlists_train, tag_cnt):
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

    return adj_tag_tag

##########################################################################################################################

def build_pop_tag(playlists_train):
    pop_tag = {}
    for playlist in playlists_train:
        L = len(playlist['tags'])
        for tag in playlist['tags']:
            if tag not in pop_tag:
                pop_tag[tag] = 0
            pop_tag[tag] += 1

    pop_tag = sorted(pop_tag.items(), key=lambda t: t[1], reverse=True)

    return pop_tag
##########################################################################################################################


def build_pop_genre_tag(playlists_train, songs):
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
        pop_genre_tag[gid] = sorted(pop_genre_tag[gid].items(), key=lambda t: t[1], reverse=True)

    return pop_genre_tag