import argparse

from datetime import date
from absl import flags

parser = argparse.ArgumentParser(description='Arguments')

# Running env
parser.add_argument('--subset', default=0,
                    type=int, help='number of playlists to check(0 means whole playlists to be tested)')

# Data & Result file path
parser.add_argument('--train', default='../data/orig/train.json',
                    type=str, help='train file path')
parser.add_argument('--valid', default='../data/questions/val.json',
                    type=str, help='valid file path')
parser.add_argument('--valid_answer', default='../data/answers/val.json',
                    type=str, help='test file path')
parser.add_argument('--test', default='../data/orig/train.json',
                    type=str, help='test file path')
parser.add_argument('--song_meta', default='../data/meta_data/song_meta.json',
                    type=str, help='song meta file path')
parser.add_argument('--genre_gn_all', default='../data/meta_data/genre_gn_all.json',
                    type=str, help='genre all path')
parser.add_argument('--result', default='result.json',
                    type=str, help='result json file path')


# Hyper parameters
parser.add_argument('--standard_date', default='1900/1/1',
                    type=str, help='standard date yyyy/m/d')
parser.add_argument('--add_valid', default=True,
                    type=bool, help='whether add valid set to factorizer or not')
parser.add_argument('--random_seed', default=525,
                    type=int, help='random seed')
parser.add_argument('--log_base', default=8,
                    type=int, help='log base for calculating denominator')
parser.add_argument('--few_artist', default=0.4,
                    type=float, help='few artist threshold')
parser.add_argument('--few_album', default=0.4,
                    type=float, help='few album threshold')
parser.add_argument('--mtag_decay_weight', default=0.5,
                    type=float, help='decay weight applied to mtag')
parser.add_argument('--tag_weight_exponent', default=0.125,
                    type=float, help='exponent number for calculating tag weight')
parser.add_argument('--dominant_artist_threshold', default=0.75,
                    type=float, help='threshold of dominant artist in a playlist')
parser.add_argument('--in_term_weight', default=2,
                    type=int, help='weight applied to in_term songs')
parser.add_argument('--found_artist_weight', default=1.5,
                    type=float, help='weight applied to songs of same artist')
parser.add_argument('--tagged_artist_weight', default=1.5,
                    type=float, help='weight applied to songs of artist mentioned in tags')
parser.add_argument('--occur_genre_weight', default=1.2,
                    type=float, help='weight applied to songs of genre occurred in other songs')
parser.add_argument('--in_tag_genre_weight', default=1.5,
                    type=float, help='weight applied to songs of genre occurred in tags')
parser.add_argument('--confidence_interval_factor', default=3,
                    type=int, help='confidence interval factor of normal distribution')
parser.add_argument('--meaning', default=30,
                    type=int, help='threshold to regard the tag as important one')

args = parser.parse_args()






