# from lib.factorization_ops import *
from lib import factorization_ops
from tqdm import tqdm
import pickle

class adjacencyMatrix:
    def __init__(self, data_loader):
        self.loader = data_loader

        self.train = data_loader.playlists_train
        self.songs = data_loader.songs
        self.genres = data_loader.genres

        # Song matrix
        self.song_cnt = {}
        self.tag_cnt = {}
        self.tags_cnt = {}
        self.adj_song = {}
        self.adj_tag = {}
        self.plist = {}
        self.plist_tag = {}
        self.adj_tag2 = {}
        self.pop = {}
        self.pop_genre = {}

        # Tag matrix
        self.adj_song_tag = {}
        self.adj_tag_tag = {}
        self.pop_tag = {}
        self.pop_genre_tag = {}


    def set_adj_matrix(self):
        self.song_cnt = factorization_ops.build_song_cnt(self.train)
        self.tag_cnt = factorization_ops.build_tag_cnt(self.train)
        self.adj_song = factorization_ops.build_adj_song(self.train, self.song_cnt)
        self.adj_tag = factorization_ops.build_adj_tag(self.train, self.tag_cnt)
        self.plist = factorization_ops.build_plist(self.train)
        self.plist_tag = factorization_ops.build_plist_tag(self.train)
        self.adj_tag2, self.tags_cnt = factorization_ops.build_adj_tag2(self.train)
        self.pop = factorization_ops.build_pop(self.train)
        self.pop_genre = factorization_ops.build_pop_genre(self.train, self.songs)

        print('ALL SONG ADJ MATRIX IS LOADED')


        # Tag matrix
        self.adj_song_tag = factorization_ops.build_adj_song_tag(self.train)
        self.adj_tag_tag = factorization_ops.build_adj_tag_tag(self.train, self.tag_cnt)
        self.pop_tag = factorization_ops.build_pop_tag(self.train)
        self.pop_genre_tag = factorization_ops.build_pop_genre_tag(self.train, self.songs)

        print('ALL TAG ADJ MATRIX IS LOADED')

        # self.song_cnt = factorization_ops.build_song_cnt(self.train)
        # with open('./pickle/tag_cnt.pkl', 'rb') as f:
        #     self.tag_cnt = pickle.load(f)
        # with open('./pickle/adj_song.pkl', 'rb') as f:
        #     self.adj_song = pickle.load(f)
        # with open('./pickle/adj_tag.pkl', 'rb') as f:
        #     self.adj_tag = pickle.load(f)
        # with open('./pickle/plist.pkl', 'rb') as f:
        #     self.plist = pickle.load(f)
        # with open('./pickle/plist_tag.pkl', 'rb') as f:
        #     self.plist_tag = pickle.load(f)
        # with open('./pickle/adj_tag2.pkl', 'rb') as f:
        #     self.adj_tag2 = pickle.load(f)
        # with open('./pickle/tags_cnt.pkl', 'rb') as f:
        #     self.tags_cnt = pickle.load(f)
        # with open('./pickle/pop.pkl', 'rb') as f:
        #     self.pop = pickle.load(f)
        # with open('./pickle/pop_genre.pkl', 'rb') as f:
        #     self.pop_genre = pickle.load(f)
        # print('ALL ADJ SONGS ARE LOADED')
        #
        #
        # with open('./pickle/adj_song_tag.pkl', 'rb') as f:
        #     self.adj_song_tag = pickle.load(f)
        # with open('./pickle/adj_tag_tag.pkl', 'rb') as f:
        #     self.adj_tag_tag = pickle.load(f)
        # with open('./pickle/pop_tag.pkl', 'rb') as f:
        #     self.pop_tag = pickle.load(f)
        # with open('./pickle/pop_genre_tag.pkl', 'rb') as f:
        #     self.pop_genre_tag = pickle.load(f)
        # print('ALL ADJ TAGS ARE LOADED')
