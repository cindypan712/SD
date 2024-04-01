import praw
from searcher import Searcher

user_info = open('user info.txt', 'r')
lines = user_info.readlines()
username = lines[0][:-1]
password = lines[1]

reddit = praw.Reddit(
    client_id='Vr5Xdhhiu1HEiLcR-t9rYQ',
    client_secret='ps4ZoQDpOOtnekU1Oiny6n4C2QHCwg',
    user_agent='socialdynamicsAPI',
    username=username,
    password=password
)

searcher = Searcher(reddit, 'Conservative')

searcher.search()

searcher.write_to()