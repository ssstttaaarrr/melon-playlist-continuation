from datetime import date
from lib.data.data_loader import *
from lib.factorization_ops import *

def set_updt_date(playlists_valq):
    for indx in range(len(playlists_valq)):
        playlist = playlists_valq[indx]
        tmp = playlist['updt_date']

        year = int(tmp[0]) * 1000 + int(tmp[1]) * 100 + int(tmp[2]) * 10 + int(tmp[3])
        month = int(tmp[5]) * 10 + int(tmp[6])
        day = int(tmp[8]) * 10 + int(tmp[9])

        isValidDate = True
        try:
            date(year, month, day)
        except ValueError:
            isValidDate = False

        if not isValidDate:
            year = 1950
            month = 1
            day = 1

        playlist['updt_date'] = date(year, month, day)


def set_issue_date(songs):
    for sid in range(len(songs)):
        tmp = songs[sid]['issue_date']

        year = int(tmp[0]) * 1000 + int(tmp[1]) * 100 + int(tmp[2]) * 10 + int(tmp[3])
        month = int(tmp[4]) * 10 + int(tmp[5])
        day = int(tmp[6]) * 10 + int(tmp[7])

        isValidDate = True
        try:
            date(year, month, day)
        except ValueError:
            isValidDate = False

        if not isValidDate:
            year = 1950
            month = 1
            day = 1

        songs[sid]['issue_date'] = date(year, month, day)

def tag_in_title(indx, data_loader, factorizer):
    playlist = data_loader.playlists_valq[indx]
    title = playlist['plylst_title']
    title = title.replace(" ", "")

    ret = []
    L = len(title)
    for i in range(L):
        for j in range(i, L):
            s = title[i:j+1]

            if s not in factorizer.tag_cnt:
                continue
            ret.append(s)
    return ret
