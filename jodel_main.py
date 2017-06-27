import os
import pickle
from JodelCrawler import JodelCrawlAcc
import time
import csv
from collections import deque

main_dir = ''
account_dir = main_dir + 'accounts/'
data_dir = main_dir + 'data/'
stats_file = main_dir + 'stats.csv'
sleep_duration = 0

# if True try to read the last post_id from file and start off where you left of
# currently NOT WORKING (jodel will just return an empty result if after= parameter post_id is too far in the past)
continue_post_id = False

post_count = 0
reset_time = time.time() + 60 * 60

jodl_accs = []

for account_file in os.listdir(account_dir):
    if account_file.endswith('.pickle'):
        acc = pickle.load(open(account_dir + account_file, 'rb'))
        # acc.racks = 1
        path = data_dir + acc.city + '.csv'
        if os.path.isfile(path):
            with open(path, 'r', newline='', encoding='utf-8') as file:
                try:
                    last_row = deque(csv.reader(file, delimiter=';'), 1)[0]
                except IndexError:  # empty file
                    last_row = None
                if last_row and continue_post_id:
                    acc.latest_post_id = last_row[0]
        jodl_accs.append(acc)

while True:
    for account in jodl_accs:
        # print(account.city)
        if isinstance(account, JodelCrawlAcc):
            account.fetch_new_posts()
            path = data_dir + account.city + '.csv'
            post_count += len(account.tracked_posts[0])
            account.drop_latest_tracked_posts(path=path)

    current_time = time.time()
    if current_time > reset_time:
        with open(stats_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([current_time, post_count])
            post_count = 0
        reset_time = current_time + 60 * 60

    # wait some time before running again
    time.sleep(sleep_duration)
