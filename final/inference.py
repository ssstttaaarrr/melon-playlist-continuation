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

    ############################ song inference ################################
    rec_songs = {}

    start = time.time()
    timer = 0
    for playlist in playlists_valq:
        if timer % 1000 == 0:
            print('timer:', timer, time.time() - start)
            start = time.time()

        pid = playlist['id']
        if testing == 1:
            rec_songs[pid] = song_continuation_ops.test(timer, data_loader, factorizer)
        # else:
        #     rec_songs[pid] = song_continuation_ops.solve(timer)

        timer += 1

    ############################ tag inference ################################
    rec_tags = {}

    timer = 0
    for playlist in playlists_valq:
        if timer % 1000 == 0:
            print('timer:', timer)

        pid = playlist['id']
        rec_tags[pid] = tag_continuation_ops.solve_tag(timer, data_loader, factorizer)
        timer += 1

    answers = []

    for playlist in playlists_valq:
        pid = playlist['id']
        answer = {'id': pid, 'songs': rec_songs[pid], 'tags': rec_tags[pid]}
        answers.append(answer)

    write_json(answers, 'results.json')


if __name__ == '__main__':
    main()
