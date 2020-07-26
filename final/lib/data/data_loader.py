from options import parser
from datetime import date
from lib.data.arena_util import load_json
from lib.playlist_ops import set_issue_date
from lib.playlist_ops import set_updt_date

args = parser.parse_args()

class melonPlaylist:
    def __init__(self):
        self.playlists_train = None
        self.playlists_valq = None
        self.playlists_vala = None
        self.songs = None
        self.genres = None
        self.meaningless = None
        self.tag_to_genre = {}
        self.tag_to_date = {}

        self.std = args.standard_date.split('/')
        self.standard = date(int(self.std[0]), int(self.std[1]), int(self.std[2]))

    def _set_meaningless(self):
        self.meaningless = {
            'R', '바', '1', 'B', '2', 'J', '3', 'v', '칠', '앙', '4', '9', '8', '6', 'I', 'd', '볾', '7', 'w', 'H', '왬'
            , 'm', '5', '0', '푹', 'N', 'C', '묩', '켄', '쎈', '팎', 'ㄹ', '으', '웅', '외', 'X', '하', '무', '냥', 'U', 'A'
            , 's', '헿', '웩', '읭', '능', '윽', '과', '뀿', '뀨', '모', '뫼', '퇼', 'y', '홓', '혀', '포', '궁', '55', '56'
            , '22', '히힝', '하핫', '2부', '40', '78', '2탄', '50', '18', '8화', 'ㅎㅎ', '4주', '13', 'or', '66', '쿄쿄'
            , '3년', '뭐지', '냠냠', '한다', '16', '98', '4화', '2주', '3초', '않는', '아녕', '54', '15', '17', '81', '47'
            , '3기', '풬킨', '2등', '히힉', '규규', '않아', '팊니', '누뉴', '77', '팊콘', '잉잉', '1주', '첫주', '빠밤'
            , '군머', '5만', '않고', '7명', '펌글', '순실', '퍽퍽', '1탄', '1년', '우앵', '노노', 'ww', '예꾸'
            , '이런', '인듯', '4슴', '외츌', '14', '33', '허허', '6화', '12', '9화', '3화', '1화', '5화', '4시'
            , '많다', '그것', '5초', 'ㅋㅋ', '2화', '1일', '7화', '30', '05', '06', '07', '매주', '아아', '00'
            , '11', '01', '02', '03', '04', '으악', '우아', '쟌디', '2426', '55', '7연속', '56', '홓'
            , '529곡', '14회'
        }

    def _set_tag_to_genre(self):
        self.tag_to_genre['힙합'] = ['GN0300', 'GN1200']
        self.tag_to_genre['락'] = ['GN0600', 'GN1000']
        self.tag_to_genre['랩'] = ['GN0300', 'GN1200']
        self.tag_to_genre['알앤비'] = ['GN0400', 'GN1300']
        self.tag_to_genre['OST'] = ['GN1500']
        self.tag_to_genre['피아노'] = ['GN1600', 'GN1800']
        self.tag_to_genre['연주곡'] = ['GN1600', 'GN1800']
        self.tag_to_genre['일렉'] = ['GN1100', 'GN2600', 'GN2700']
        self.tag_to_genre['클래식'] = ['GN1600', 'GN1800']
        self.tag_to_genre['EDM'] = ['GN1100', 'GN2600', 'GN2700']
        self.tag_to_genre['RnB'] = ['GN0400', 'GN1300']
        self.tag_to_genre['일렉트로니카'] = ['GN1100', 'GN2600', 'GN2700']
        self.tag_to_genre['록'] = ['GN0600', 'GN1000']
        self.tag_to_genre['감성힙합'] = ['GN0300', 'GN1200']
        self.tag_to_genre['CCM'] = ['GN2100']
        self.tag_to_genre['Rock'] = ['GN0600', 'GN1000']
        self.tag_to_genre['JPOP'] = ['GN1900']
        self.tag_to_genre['HipHip'] = ['GN0300', 'GN1200']
        self.tag_to_genre['트로트'] = ['GN0700']
        self.tag_to_genre['electronica'] = ['GN1100', 'GN2600', 'GN2700']
        self.tag_to_genre['걸그룹'] = ['GN2500']
        self.tag_to_genre['국내힙합'] = ['GN0300', 'GN1200']
        self.tag_to_genre['드라마'] = ['GN1500']
        self.tag_to_genre['영화'] = ['GN1500']
        self.tag_to_genre['일렉트로닉'] = ['GN1100', 'GN2600', 'GN2700']
        self.tag_to_genre['외힙'] = ['GN0300', 'GN1200']
        self.tag_to_genre['메탈'] = ['GN0600', 'GN1000']
        self.tag_to_genre['외국힙합'] = ['GN0300', 'GN1200']
        self.tag_to_genre['감성발라드'] = ['GN0100']
        self.tag_to_genre['국힙'] = ['GN0300', 'GN1200']
        self.tag_to_genre['영화음악'] = ['GN1500']
        self.tag_to_genre['영화OST'] = ['GN1500']
        self.tag_to_genre['RNBSOUL'] = ['GN0400', 'GN1300']
        self.tag_to_genre['팝송추천'] = ['GN0900', 'GN1900']
        self.tag_to_genre['동요'] = ['GN2200']
        self.tag_to_genre['한국힙합'] = ['GN0300', 'GN1200']
        self.tag_to_genre['드라마ost'] = ['GN1500']
        self.tag_to_genre['알엔비'] = ['GN0400', 'GN1300']
        self.tag_to_genre['찬양'] = ['GN2100']
        self.tag_to_genre['피아노연주곡'] = ['GN1600', 'GN1800']
        self.tag_to_genre['보이그룹'] = ['GN2500']
        self.tag_to_genre['쇼미더머니'] = ['GN0300', 'GN1200']
        self.tag_to_genre['록메탈'] = ['GN0600', 'GN1000']
        self.tag_to_genre['남자아이돌'] = ['GN2500']
        self.tag_to_genre['해외힙합'] = ['GN0300', 'GN1200']
        self.tag_to_genre['일본'] = ['GN1900']
        self.tag_to_genre['제이팝'] = ['GN1900']
        self.tag_to_genre['Electronic'] = ['GN1100', 'GN2600', 'GN2700']
        self.tag_to_genre['ASMR'] = ['GN2800']


    def _set_tag_to_date(self):
        self.tag_to_date['2000년대'] = (date(1995, 1, 1), date(2015, 1, 1))
        self.tag_to_date['2000'] = (date(1995, 1, 1), date(2015, 1, 1))
        self.tag_to_date['1990년대'] = (date(1985, 1, 1), date(2005, 1, 1))
        self.tag_to_date['90년대'] = (date(1985, 1, 1), date(2005, 1, 1))
        self.tag_to_date['1990'] = (date(1985, 1, 1), date(2005, 1, 1))
        self.tag_to_date['2010년대'] = (date(2005, 1, 1), date(2025, 1, 1))
        self.tag_to_date['2010'] = (date(2005, 1, 1), date(2025, 1, 1))
        self.tag_to_date['2019'] = (date(2019, 1, 1), date(2020, 1, 1))
        self.tag_to_date['7080'] = (date(1965, 1, 1), date(1995, 1, 1))
        self.tag_to_date['1970_80'] = (date(1965, 1, 1), date(1995, 1, 1))
        self.tag_to_date['1980'] = (date(1975, 1, 1), date(1995, 1, 1))
        self.tag_to_date['2017'] = (date(2017, 1, 1), date(2018, 1, 1))
        self.tag_to_date['2020'] = (date(2020, 1, 1), date(2021, 1, 1))
        self.tag_to_date['8090'] = (date(1975, 1, 1), date(2005, 1, 1))
        self.tag_to_date['2018'] = (date(2018, 1, 1), date(2019, 1, 1))
        self.tag_to_date['80년대'] = (date(1975, 1, 1), date(1995, 1, 1))


    # load train/valid data & set tag2genre, tag2date
    def load_dataset(self):
        self.playlists_train = load_json(args.train)
        self.playlists_valq = load_json(args.valid)
        self.playlists_vala = load_json(args.valid_answer)
        self.playlists_test = load_json(args.test)

        self.songs = load_json(args.song_meta)
        self.genres = load_json(args.genre_gn_all)

        if args.add_valid:
            self.playlists_train += self.playlists_valq
            self.playlists_train += self.playlists_test

        self._set_tag_to_genre()
        self._set_tag_to_date()
        self._set_meaningless()

        set_issue_date(self.songs)
        set_updt_date(self.playlists_valq)

        print('The number of PlayLists to train: ', len(self.playlists_train))

        return self.playlists_train, self.playlists_valq, self.playlists_vala, self.songs, self.genres

