from lib.data.data_loader import *
from lib.factorization_ops import *
from lib.playlist_ops import tag_in_title

import numpy as np
import math

args = parser.parse_args()

# std = args.standard_date.split('/')
# standard = date(std[0], std[1], std[2])


def add_tag(indx, ret, score, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    more_tag = tag_in_title(indx, data_loader, factorizer)

    for tag in more_tag:
        if tag in score:
            score[tag] *= 4

    score = sorted(score.items(), key=lambda t: t[1], reverse=True)

    for i in range(len(score)):
        if len(ret) == 10:
            break
        if (score[i][0] in playlist['tags']) or (score[i][0] in ret):
            continue

        ret.append(score[i][0])


def complete_tag(indx, ret, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    genre_score = {}
    tot = len(playlist['songs'])

    for sid in playlist['songs']:
        for gid in factorizer.songs[sid]['song_gn_gnr_basket']:
            if gid not in genre_score:
                genre_score[gid] = 0
            genre_score[gid] += 1 / tot

    max_genre_score = 0
    max_genre = -1
    for key, value in genre_score.items():
        if max_genre_score < value:
            max_genre_score = value
            max_genre = key

    if max_genre in factorizer.pop_genre_tag:
        for i in range(len(factorizer.pop_genre_tag[max_genre])):
            if len(ret) == 10:
                break
            if (factorizer.pop_genre_tag[max_genre][i][0] in playlist['tags']) or \
                    (factorizer.pop_genre_tag[max_genre][i][0] in ret):
                continue

            ret.append(factorizer.pop_genre_tag[max_genre][i][0])

    for i in range(len(factorizer.pop_tag)):
        if len(ret) == 10:
            break
        if (factorizer.pop_tag[i][0] in playlist['tags']) or (factorizer.pop_tag[i][0] in ret):
            continue

        ret.append(factorizer.pop_tag[i][0])


# In[716]:


def solve_tag_no_info(indx, data_loader, factorizer):
    ret = []

    more_tag = tag_in_title(indx, data_loader, factorizer)

    score = {}
    for mtag in more_tag:
        w = np.power(factorizer.tag_cnt[mtag], 0.5)
        for key, val in factorizer.adj_tag_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w

    add_tag(indx, ret, score, data_loader, factorizer)

    if len(ret) == 10:
        return ret

    complete_tag(indx, ret, data_loader, factorizer)
    return ret


def solve_tag_only_song(indx, data_loader, factorizer):
    ret = []

    playlist = data_loader.playlists_valq[indx]

    occur = {}
    for sid in playlist['songs']:
        if sid not in factorizer.plist:
            continue

        L = len(factorizer.plist[sid])
        for pid in factorizer.plist[sid]:
            if pid not in occur:
                occur[pid] = 0
            occur[pid] += 1 / math.log(7 + L, 8)

    for tag in playlist['tags']:
        L = len(factorizer.plist_tag[tag])

        for key in factorizer.plist_tag[tag]:
            if key not in occur:
                # occur[key] = 0
                continue
            occur[key] += 1.2 * 1 / math.log(7 + L)

    more_tag = tag_in_title(indx, data_loader, factorizer)

    for tag in more_tag:
        L = len(factorizer.plist_tag[tag])

        for key in factorizer.plist_tag[tag]:
            if key not in occur:
                # occur[key] = 0
                continue
            occur[key] += 1.2 * 1 / math.log(7 + L)

    score = {}
    for key, val in occur.items():
        if val < 0.333:
            continue

        p = data_loader.playlists_train[key]
        w = np.power(val, 4)

        for tag in p['tags']:
            if tag not in score:
                score[tag] = 0
            score[tag] += w

    add_tag(indx, ret, score, data_loader, factorizer)

    if len(ret) == 10:
        return ret

    more_tag = tag_in_title(indx, data_loader, factorizer)

    score = {}
    for mtag in more_tag:
        w = np.power(factorizer.tag_cnt[mtag], 0.5)
        for key, val in factorizer.adj_tag_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w

    add_tag(indx, ret, score, data_loader, factorizer)

    if len(ret) == 10:
        return ret

    complete_tag(indx, ret, data_loader, factorizer)
    return ret


def solve_tag_main(indx, data_loader, factorizer):
    ret = []

    playlist = data_loader.playlists_valq[indx]

    score = {}
    for tag in playlist['tags']:
        if tag not in factorizer.adj_tag_tag:
            continue

        for key, val in factorizer.adj_tag_tag[tag].items():
            if val < 0.333:
                continue

            w = np.power(val, 0.125)

            if key not in score:
                score[key] = 0
            score[key] += w

    add_tag(indx, ret, score, data_loader, factorizer)

    if len(ret) == 10:
        return ret

    occur = {}
    for sid in playlist['songs']:
        if sid not in factorizer.plist:
            continue

        L = len(factorizer.plist[sid])
        for pid in factorizer.plist[sid]:
            if pid not in occur:
                occur[pid] = 0
            occur[pid] += 1 / math.log(7 + L, 8)

    for tag in playlist['tags']:
        L = len(factorizer.plist_tag[tag])

        for key in factorizer.plist_tag[tag]:
            if key not in occur:
                # occur[key] = 0
                continue
            occur[key] += 1.2 * 1 / math.log(7 + L)

    more_tag = tag_in_title(indx, data_loader, factorizer)

    for tag in more_tag:
        L = len(factorizer.plist_tag[tag])

        for key in factorizer.plist_tag[tag]:
            if key not in occur:
                # occur[key] = 0
                continue
            occur[key] += 1.2 * 1 / math.log(7 + L)

    score = {}
    for key, val in occur.items():
        if val < 0.333:
            continue

        p = data_loader.playlists_train[key]
        w = np.power(val, 4)

        for tag in p['tags']:
            if tag not in score:
                score[tag] = 0
            score[tag] += w

    add_tag(indx, ret, score, data_loader, factorizer)

    if len(ret) == 10:
        return ret

    more_tag = tag_in_title(indx, data_loader, factorizer)

    score = {}
    for mtag in more_tag:
        w = np.power(factorizer.tag_cnt[mtag], 0.5)
        for key, val in factorizer.adj_tag_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w

    add_tag(indx, ret, score, data_loader, factorizer)

    if len(ret) == 10:
        return ret

    complete_tag(indx, ret, data_loader, factorizer)
    return ret


def solve_tag(indx, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    if len(playlist['songs']) == 0 and len(playlist['tags']) == 0:
        return solve_tag_no_info(indx, data_loader, factorizer)
    elif len(playlist['tags']) == 0:
        return solve_tag_only_song(indx, data_loader, factorizer)
    else:
        return solve_tag_main(indx, data_loader, factorizer)
