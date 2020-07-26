from options import parser
from datetime import date
# from lib.data.data_loader import playlists_train
# from lib.data.data_loader import playlists_valq
# from lib.data.data_loader import playlists_vala
# from lib.data.data_loader import tag_to_genre
# from lib.data.data_loader import tag_to_date
# from lib.data.data_loader import songs

# from lib.data.data_loader import playlists_train
# from lib.data.data_loader import playlists_valq
# from lib.data.data_loader import playlists_vala

from lib.factorization_ops import *
from lib.playlist_ops import tag_in_title
# from lib.factorization_ops import pop
# from lib.factorization_ops import tag_cnt

import numpy as np
import math

args = parser.parse_args()

# std = args.standard_date.split('/')
# std = list(map(int, std))
# standard = date(std[0], std[1], std[2])


def possible(indx, sid, playlists_valq, songs):
    playlist = playlists_valq[indx]
    return songs[sid]['issue_date'] <= playlist['updt_date']


def in_term(date, mean, var, data_loader):
    width = args.confidence_interval_factor
    return mean - width * np.sqrt(var) <= (date - data_loader.standard).days and \
           (date - data_loader.standard).days <= mean + width * np.sqrt(var)


def in_range(pop_cnt, pop_mean, pop_var):
    width = args.confidence_interval_factor
    return pop_mean - width * np.sqrt(pop_var) <= pop_cnt and pop_cnt <= pop_mean + width * np.sqrt(pop_var)


def allowed_genre(sid, appear, factorizer):
    for gid in factorizer.songs[sid]['song_gn_gnr_basket']:
        if gid in appear:
            return True
    return False


def allowed_term(sid, term, factorizer):
    for d in term:
        if d[0] <= factorizer.songs[sid]['issue_date'] and factorizer.songs[sid]['issue_date'] <= d[1]:
            return True
    return False


def few_artist(indx, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    artist_score = {}
    tot = len(playlist['songs'])

    cnt = 0
    for sid in playlist['songs']:
        for aid in factorizer.songs[sid]['artist_id_basket']:
            if aid not in artist_score:
                artist_score[aid] = 1

    return (tot != 0) and (len(artist_score) / tot < args.few_artist)


def few_album(indx, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    album_score = {}
    tot = len(playlist['songs'])

    for sid in playlist['songs']:
        aid = factorizer.songs[sid]['album_id']
        if aid not in album_score:
            album_score[aid] = 1

    return (tot != 0) and (len(album_score) / tot < args.few_album)


def is_our_artist(sid, artists, factorizer):
    for aid in artists:
        if aid in factorizer.songs[sid]['artist_id_basket']:
            return True
    return False


def is_our_album(sid, albums, factorizer):
    return (factorizer.songs[sid]['album_id'] in albums)


def max_artist(indx, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    artist = {}
    for sid in playlist['songs']:
        for aid in factorizer.songs[sid]['artist_id_basket']:
            if aid not in artist:
                artist[aid] = 0
            artist[aid] += 1

    artist = sorted(artist.items(), key=lambda t: t[1], reverse=True)

    if len(artist) == 0:
        return 0, 0
    else:
        return artist[0][0], artist[0][1] / len(playlist['songs'])


def add(indx, ret, score, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    mean = 0
    var = 0

    if len(playlist['songs']) == 0:
        mean = 0
        var = 100000000000
    else:
        for sid in playlist['songs']:
            mean += (factorizer.songs[sid]['issue_date'] - data_loader.standard).days
        mean /= len(playlist['songs'])

        for sid in playlist['songs']:
            var += np.power((factorizer.songs[sid]['issue_date'] - data_loader.standard).days - mean, 2)
        var /= len(playlist['songs'])

    pop_mean = 0
    pop_var = 0

    if len(playlist['songs']) == 0:
        pop_mean = 0
        pop_var = 10000000000000
    else:
        for sid in playlist['songs']:
            pop_mean += factorizer.song_cnt[sid]
        pop_mean /= len(playlist['songs'])

        for sid in playlist['songs']:
            pop_var += np.power(factorizer.song_cnt[sid] - pop_mean, 2)
        pop_var /= len(playlist['songs'])


    ########################################################################################

    appear = []
    for tag in playlist['tags']:
        if tag in data_loader.tag_to_genre:
            appear += data_loader.tag_to_genre[tag]

    more_tag = tag_in_title(indx, data_loader, factorizer)
    for tag in more_tag:
        if tag in data_loader.tag_to_genre:
            appear.append(data_loader.tag_to_genre[tag])

    term = []
    for tag in playlist['tags']:
        if tag in data_loader.tag_to_date:
            term.append(data_loader.tag_to_date[tag])

    artists = {}
    for sid in playlist['songs']:
        for aid in factorizer.songs[sid]['artist_id_basket']:
            if aid not in artists:
                artists[aid] = 0
            artists[aid] += 1

    albums = {}
    for sid in playlist['songs']:
        aid = factorizer.songs[sid]['album_id']
        if aid not in albums:
            albums[aid] = 0
        albums[aid] += 1

    is_few_artist = few_artist(indx, data_loader, factorizer)
    is_few_album = few_album(indx, data_loader, factorizer)

    who, how = max_artist(indx, data_loader, factorizer)

    dom = 0
    if how > args.dominant_artist_threshold:
        dom = 1

    for key in score:
        if in_term(factorizer.songs[key]['issue_date'], mean, var, data_loader):
            score[key] *= args.in_term_weight

    for key in score:
        found = False
        for aid in factorizer.songs[key]['artist_id_basket']:
            if aid in artists:
                found = True
                break
        if found:
            score[key] *= args.found_artist_weight

    for key in score:
        for name in factorizer.songs[key]['artist_name_basket']:
            if (name in playlist['tags']) or (name in more_tag):
                score[key] *= args.tagged_artist_weight

    occur_genre = {}
    for sid in playlist['songs']:
        for gid in factorizer.songs[sid]['song_gn_gnr_basket']:
            if gid not in occur_genre:
                occur_genre[gid] = 0
            occur_genre[gid] += 1

    for key in score:
        found = 0
        for gid in factorizer.songs[key]['song_gn_gnr_basket']:
            if gid in occur_genre:
                found = 1
                break

        if found == 1:
            score[key] *= args.occur_genre_weight

    for key in score:
        found = 0
        for gid in factorizer.songs[key]['song_gn_gnr_basket']:
            if gid in appear:
                found = 1
                break
        if found == 1:
            score[key] *= args.in_tag_genre_weight

    #######################################

    score = sorted(score.items(), key=lambda t: t[1], reverse=True)

    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or \
                (not possible(indx, score[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        if is_few_artist and (not is_our_artist(score[i][0], artists, factorizer)):
            continue
        if is_few_album and (not is_our_album(score[i][0], albums, factorizer)):
            continue
        if (dom == 1) and (who not in factorizer.songs[score[i][0]]['artist_id_basket']):
            continue

        ret.append(score[i][0])

    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or \
                (not possible(indx, score[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        if (dom == 1) and (who not in factorizer.songs[score[i][0]]['artist_id_basket']):
            continue

        ret.append(score[i][0])

    return mean, var


def complete(indx, ret, mean, var, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    # mean = 0
    # var = 0
    #
    # if len(playlist['songs']) == 0:
    #     mean = 0
    #     var = 1000000000
    # else:
    #     for sid in playlist['songs']:
    #         mean += (songs[sid]['issue_date'] - standard).days
    #     mean /= len(playlist['songs'])
    #
    #     for sid in playlist['songs']:
    #         var += np.power((songs[sid]['issue_date'] - standard).days - mean, 2)
    #     var /= len(playlist['songs'])

    # pop_mean = 0
    # pop_var = 0
    #
    # if len(playlist['songs']) == 0:
    #     pop_mean = 0
    #     pop_var = 10000000000000
    # else:
    #     for sid in playlist['songs']:
    #         pop_mean += song_cnt[sid]
    #     pop_mean /= len(playlist['songs'])
    #
    #     for sid in playlist['songs']:
    #         pop_var += np.power(song_cnt[sid] - pop_mean, 2)
    #     pop_var /= len(playlist['songs'])
    ########################################################################################

    appear = []
    for tag in playlist['tags']:
        if tag in data_loader.tag_to_genre:
            appear += data_loader.tag_to_genre[tag]

    more_tag = tag_in_title(indx, data_loader, factorizer)
    for tag in more_tag:
        if tag in data_loader.tag_to_genre:
            appear.append(data_loader.tag_to_genre[tag])

    term = []
    for tag in playlist['tags']:
        if tag in data_loader.tag_to_date:
            term.append(data_loader.tag_to_date[tag])

    artists = []
    for sid in playlist['songs']:
        for aid in factorizer.songs[sid]['artist_id_basket']:
            artists.append(aid)

    albums = {}
    for sid in playlist['songs']:
        aid = factorizer.songs[sid]['album_id']
        if aid not in albums:
            albums[aid] = 1

    is_few_artist = few_artist(indx, data_loader, factorizer)
    is_few_album = few_album(indx, data_loader, factorizer)

    who, how = max_artist(indx, data_loader, factorizer)

    dom = 0
    if how > args.dominant_artist_threshold:
        dom = 1

    ################ get max genre

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

    for i in range(len(factorizer.pop)):
        if len(ret) == 100:
            break
        if (factorizer.pop[i][0] in playlist['songs']) or (factorizer.pop[i][0] in ret) or \
                (not possible(indx, factorizer.pop[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        if not in_term(factorizer.songs[factorizer.pop[i][0]]['issue_date'], mean, var, data_loader):
            continue
        if is_few_artist and (not is_our_artist(factorizer.pop[i][0], artists, factorizer)):
            continue
        if is_few_album and (not is_our_album(factorizer.pop[i][0], albums, factorizer)):
            continue
        if (dom == 1) and (who not in factorizer.songs[factorizer.pop[i][0]]['artist_id_basket']):
            continue

        ret.append(factorizer.pop[i][0])

    for i in range(len(factorizer.pop)):
        if len(ret) == 100:
            break
        if (factorizer.pop[i][0] in playlist['songs']) or (factorizer.pop[i][0] in ret) or \
                (not possible(indx, factorizer.pop[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        if not in_term(factorizer.songs[factorizer.pop[i][0]]['issue_date'], mean, var, data_loader):
            continue
        if (dom == 1) and (who not in factorizer.songs[factorizer.pop[i][0]]['artist_id_basket']):
            continue

        ret.append(factorizer.pop[i][0])

    for i in range(len(factorizer.pop)):
        if len(ret) == 100:
            break
        if (factorizer.pop[i][0] in playlist['songs']) or (factorizer.pop[i][0] in ret) or \
                (not possible(indx, factorizer.pop[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        ret.append(factorizer.pop[i][0])

# In[914]:


def solve_no_info(indx, data_loader, factorizer):
    ret = []

    more_tag = tag_in_title(indx, data_loader, factorizer)

    score = {}
    for mtag in more_tag:
        w = np.power(factorizer.tag_cnt[mtag], args.mtag_decay_weight)
        for key, val in factorizer.adj_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w

    mean, var = add(indx, ret, score, data_loader, factorizer)

    if len(ret) == 100:
        return ret

    complete(indx, ret, mean, var, data_loader, factorizer)
    return ret


def solve_one_tag(indx, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]
    ret = []
    tag = playlist['tags'][0]

    score = {}
    for key, val in factorizer.adj_tag[tag].items():
        score[key] = val

    add(indx, ret, score, data_loader, factorizer)

    if len(ret) == 100:
        return ret

    occur = {}
    for sid in ret:
        L = len(factorizer.plist[sid])
        for key in factorizer.plist[sid]:
            if key not in occur:
                occur[key] = 0
            occur[key] += 1 / math.log(7 + L, args.log_base)

    score = {}
    for key, value in occur.items():
        p = data_loader.playlists_train[key]
        w = np.power(value, 4)

        for sid in p['songs']:
            if sid not in score:
                score[sid] = 0
            score[sid] += w

    add(indx, ret, score, data_loader, factorizer)

    if len(ret) == 100:
        return ret

    more_tag = tag_in_title(indx, data_loader, factorizer)

    score = {}
    for mtag in more_tag:
        w = np.power(factorizer.tag_cnt[mtag], 0.5)
        for key, val in factorizer.adj_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w

    mean, var = add(indx, ret, score, data_loader, factorizer)

    if len(ret) == 100:
        return ret

    # complete(indx, ret, score)
    complete(indx, ret, mean, var, data_loader, factorizer)
    return ret


def solve_two_tag(indx, data_loader, factorizer):
    ret = []

    playlist = data_loader.playlists_valq[indx]

    tag1 = playlist['tags'][0]
    tag2 = playlist['tags'][1]

    if tag1 > tag2:
        tag1, tag2 = tag2, tag1

    meaning = args.meaning
    if factorizer.tag_cnt[tag1] > meaning and factorizer.tag_cnt[tag2] > meaning:
        w1 = np.power(factorizer.tag_cnt[tag1], args.tag_weight_exponent)
        w2 = np.power(factorizer.tag_cnt[tag2], args.tag_weight_exponent)

        intersection = {}
        for sid in factorizer.adj_tag[tag1]:
            if sid in factorizer.adj_tag[tag2]:
                intersection[sid] = factorizer.adj_tag[tag1][sid] * w1 + factorizer.adj_tag[tag2][sid] * w2

        add(indx, ret, intersection, data_loader, factorizer)

        if len(ret) == 100:
            return ret

    occur_tag = {}
    for tag in playlist['tags']:
        L = len(factorizer.plist_tag[tag])

        for key in factorizer.plist_tag[tag]:
            if key not in occur_tag:
                occur_tag[key] = 0
            occur_tag[key] += 1 / math.log(7 + L, args.log_base)

    score = {}
    for key, value in occur_tag.items():
        p = data_loader.playlists_train[key]
        w = np.power(value, 4)

        for sid in p['songs']:
            if sid not in score:
                score[sid] = 0
            score[sid] += w

    add(indx, ret, score, data_loader, factorizer)

    if len(ret) == 100:
        return ret

    more_tag = tag_in_title(indx, data_loader, factorizer)

    score = {}
    for mtag in more_tag:
        w = np.power(factorizer.tag_cnt[mtag], 0.5)
        for key, val in factorizer.adj_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w

    mean, var = add(indx, ret, score, data_loader, factorizer)

    if len(ret) == 100:
        return ret

    complete(indx, ret, mean, var, data_loader, factorizer)
    return ret




def solve_several_tag(indx, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    ret = []

    score = {}
    for i in range(len(playlist['tags'])):
        for j in range(i + 1, len(playlist['tags'])):
            tag1 = playlist['tags'][i]
            tag2 = playlist['tags'][j]

            if tag1 > tag2:
                tag1, tag2 = tag2, tag1

            if (tag1, tag2) not in factorizer.adj_tag2:
                continue

            w = np.power(factorizer.tags_cnt[(tag1, tag2)], args.tag_weight_exponent)

            for sid in factorizer.adj_tag2[(tag1, tag2)]:
                if sid not in score:
                    score[sid] = 0
                score[sid] += np.power(factorizer.adj_tag2[(tag1, tag2)][sid], args.tag_weight_exponent) * w

    score = sorted(score.items(), key=lambda t: t[1], reverse=True)

    for i in range(len(score)):
        if score[i][1] == 0:
            break
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or \
                (not possible(indx, score[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        ret.append(score[i][0])

    if len(ret) == 100:
        return ret

    score = {}
    occur_tag = {}
    for tag in playlist['tags']:
        L = len(factorizer.plist_tag[tag])

        for key in factorizer.plist_tag[tag]:
            if key not in occur_tag:
                occur_tag[key] = 0
            occur_tag[key] += 1 / math.log(7 + L, args.log_base)

    for key, value in occur_tag.items():
        p = data_loader.playlists_train[key]
        w = np.power(value, 4)

        for sid in p['songs']:
            if sid not in score:
                score[sid] = 0
            score[sid] += w

    score = sorted(score.items(), key=lambda t: t[1], reverse=True)

    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or \
                (not possible(indx, score[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        ret.append(score[i][0])

    if len(ret) == 100:
        return ret

    score = {}
    for tag in playlist['tags']:
        w = np.power(factorizer.tag_cnt[tag], args.tag_weight_exponent)
        for sid in factorizer.adj_tag[tag]:
            if sid not in score:
                score[sid] = 0
            score[sid] += np.power(factorizer.adj_tag[tag][sid], args.tag_weight_exponent) * w
    score = sorted(score.items(), key=lambda t: t[1], reverse=True)

    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or \
                (not possible(indx, score[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        ret.append(score[i][0])

    if len(ret) == 100:
        return ret

    more_tag = tag_in_title(indx, data_loader, factorizer)

    score = {}
    for mtag in more_tag:
        w = np.power(factorizer.tag_cnt[mtag], args.mtag_decay_weight)
        for key, val in factorizer.adj_tag[mtag].items():
            if key not in score:
                score[key] = 0
            score[key] += val * w
    score = sorted(score.items(), key=lambda t: t[1], reverse=True)

    for i in range(len(score)):
        if len(ret) == 100:
            break
        if (score[i][0] in playlist['songs']) or (score[i][0] in ret) or \
                (not possible(indx, score[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        ret.append(score[i][0])

    for i in range(len(factorizer.pop)):
        if len(ret) == 100:
            break
        if (factorizer.pop[i][0] in playlist['songs']) or (factorizer.pop[i][0] in ret) or \
                (not possible(indx, factorizer.pop[i][0], data_loader.playlists_valq, factorizer.songs)):
            continue
        ret.append(factorizer.pop[i][0])

    return ret


def solve_only_tag(indx, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    if len(playlist['tags']) == 0:
        return solve_no_info(indx, data_loader, factorizer)
    elif len(playlist['tags']) == 1:
        return solve_one_tag(indx, data_loader, factorizer)
    elif len(playlist['tags']) == 2:
        return solve_two_tag(indx, data_loader, factorizer)
    else:
        return solve_several_tag(indx, data_loader, factorizer)


def solve_main(indx, data_loader, factorizer):
    ret = []
    playlist = data_loader.playlists_valq[indx]

    #######################################

    occur = {}
    for sid in playlist['songs']:
        if sid not in factorizer.plist:
            continue

        L = len(factorizer.plist[sid])
        for pid in factorizer.plist[sid]:
            if pid not in occur:
                occur[pid] = 0
            occur[pid] += 1 / math.log(7 + L, args.log_base)

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

        for sid in p['songs']:
            if sid not in score:
                score[sid] = 0
            score[sid] += w

    score2 = {}
    for sid1 in playlist['songs']:
        for sid2, val in factorizer.adj_song[sid1].items():
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

    add(indx, ret, score, data_loader, factorizer)

    if len(ret) == 100:
        return ret

    score = {}
    for sid1 in playlist['songs']:
        for sid2, val in factorizer.adj_song[sid1].items():
            w = np.power(1 + val, 0.125)

            if sid2 not in score:
                score[sid2] = 0
            score[sid2] += w

    mean, var = add(indx, ret, score, data_loader, factorizer)

    if len(ret) == 100:
        return ret

    complete(indx, ret, mean, var, data_loader, factorizer)
    return ret

# def solve(indx, data_loader, factorizer):
#     playlist = data_loader.playlists_valq[indx]
#
#     if len(playlist['songs']) == 0:
#         return solve_only_tag(indx, data_loader, factorizer)
#     else:
#         return solve_main(indx, data_loader, factorizer)


def test(indx, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]

    if len(playlist['songs']) == 0:
        return solve_only_tag(indx, data_loader, factorizer)
    # elif len(playlist['tags']) == 0:
    #    return []
    else:
        return solve_main(indx, data_loader, factorizer)



