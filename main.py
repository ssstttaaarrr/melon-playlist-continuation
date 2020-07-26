from options import parser
from lib.data.data_loader import melonPlaylist
from lib.adjacency_matrix import adjacencyMatrix
from lib import factorization_ops
from lib import song_continuation_ops
from lib.data.arena_util import write_json
from lib import tag_continuation_ops

import time
import numpy as np

args = parser.parse_args()

testing = 1
VAL_TEST_SIZE = 2000000

def main():
    # Build adjacency matrix & meta data

    data_loader = melonPlaylist()
    data_loader.load_dataset()

    factorizer = adjacencyMatrix(data_loader)
    print('Start to build adjacency matrix')
    factorizer.set_adj_matrix()

    playlists_valq = data_loader.playlists_valq
    playlists_vala = data_loader.playlists_vala

    songs = data_loader.songs

    ################## answer dic
    rec_songs = {}

    start = time.time()
    timer = 0
    checked = 0

    tot_time = time.time()
    for playlist in playlists_valq:
        if testing == 1 and timer == VAL_TEST_SIZE:
            break

        if timer % 500 == 0:
            print('timer:', timer, time.time() - start)
            start = time.time()

        # if len(playlist['songs']) != 0:
        #     timer += 1
        #     continue
        # if len(playlist['tags']) != 0:
        #     timer += 1
        #     continue

        checked += 1
        pid = playlist['id']
        if testing == 1:
            rec_songs[pid] = song_continuation_ops.test(timer, data_loader, factorizer)
        else:
            rec_songs[pid] = song_continuation_ops.solve(timer, data_loader, factorizer)

        timer += 1

    print('{} inference time: {}'.format(VAL_TEST_SIZE, time.time() - tot_time))
    print('CHECKED SONGS: ', checked)
    # In[918]:

    total_score = 0

    tt = 0
    indx = -1
    for playlist in playlists_vala:
        indx += 1
        pid = playlist['id']

        if pid not in rec_songs:
            continue
        if len(rec_songs[pid]) == 0:
            continue

        local_score = 0
        sum_score = 0
        for i in range(len(rec_songs[pid])):
            sid = rec_songs[pid][i]
            if sid in playlist['songs']:
                local_score += 1 / np.log2(i + 2)
                # print(pid, i)

        for i in range(len(playlist['songs'])):
            sum_score += 1 / np.log2(i + 2)

        total_score += local_score / sum_score

        observing = 0
        if observing == 1:
            if local_score / sum_score < 0.3 and local_score / sum_score > 0.1:
                print('~~~~~~~~~~~~', playlist['plylst_title'])
                print(local_score / sum_score)
                print('few artist? ', song_continuation_ops.few_artist(indx, data_loader, factorizer))
                print('few album?', song_continuation_ops.few_album(indx, data_loader, factorizer))
                for sid in playlists_valq[indx]['songs']:
                    print(songs[sid]['song_name'], songs[sid]['artist_name_basket'], songs[sid]['song_gn_gnr_basket'])
                print(playlist['tags'])
                for sid in playlist['songs']:
                    print(songs[sid]['song_name'], songs[sid]['artist_name_basket'], songs[sid]['song_gn_gnr_basket'])
                print('-----------------')
                for sid in rec_songs[pid]:
                    print(songs[sid]['song_name'], songs[sid]['artist_name_basket'], songs[sid]['song_gn_gnr_basket'],
                          (sid in playlists_vala[indx]['songs']))
                print('#################')

        tt += 1

    print(total_score / len(playlists_vala))
    print(total_score / tt)


    ############################ tag inference ################################
    rec_tags = {}
    timer = 0
    for playlist in playlists_valq:
        if testing == 1 and timer == VAL_TEST_SIZE:
            break

        if timer % 500 == 0:
            print('timer:', timer)

        pid = playlist['id']
        rec_tags[pid] = tag_continuation_ops.solve_tag(timer, data_loader, factorizer)
        timer += 1

    total_score = 0
    tt = 0
    for playlist in playlists_vala:
        pid = playlist['id']

        if pid not in rec_tags:
            continue

        local_score = 0
        sum_score = 0
        for i in range(len(rec_tags[pid])):
            tag = rec_tags[pid][i]
            if tag in playlist['tags']:
                local_score += 1 / np.log2(i + 2)

        for i in range(len(playlist['tags'])):
            sum_score += 1 / np.log2(i + 2)

        # if (0.01 < local_score / sum_score) and (local_score / sum_score < 0.1):
        #    print(rec_tags[pid], playlist['tags'], playlist['plylst_title'])

        total_score += local_score / sum_score
        tt += 1

    print(total_score / len(playlists_vala))
    print(total_score / tt)

    answers = []

    print('playlistQ: ', len(playlists_valq))
    print('playlistA: ', len(playlists_vala))


    c = 0
    m = 0
    for playlist in playlists_valq:
        pid = playlist['id']
        try:
            answer = {'id': pid, 'songs': rec_songs[pid], 'tags': rec_tags[pid]}
            answers.append(answer)
            c += 1
        except:
            m += 1
            # print('pid {} is missed!'.format(pid))

        # answers.append(answer)

    print('checked: ', c)
    print('missed: ', m)

    write_json(answers, 'answer1')


if __name__ == '__main__':
    main()
