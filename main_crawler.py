import JodelCrawler
import sqlite3
import pickle
import os
import time
import directories

main_dir = directories.main_dir
account_dir = directories.account_dir
data_base_dir = directories.data_base_dir

batch_size = 100

jodel_accounts = []
posts_for_database = []

for account_file in os.listdir(account_dir):
    if account_file.endswith('.pickle'):
        acc = pickle.load(open(account_dir + account_file, 'rb'))
        jodel_accounts.append(acc)


for account in jodel_accounts:
    if isinstance(account, JodelCrawler.JodelCrawlAcc):
        posts = account.get_posts_recent(skip=0, limit=batch_size)
        if posts[0] == 200:
            for post in posts:
                processed_post = [post['post_id'], int(time.time()), account.city, post['created_at'], post['message'],
                                  post['color'], post['vote_count'], post['pin_count'], post['child_count']]
                posts_for_database.append(processed_post)

        elif posts[0] == 401:
            account.refresh_access_token()

        else:
            print('Failed to fetch new posts. Error Code', posts[0])

# open connection to database
connection = sqlite3.connect(database=data_base_dir)

with connection:
    cursor = connection.cursor()
    # create table if none exists
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (post_id text UNIQUE, fetched_at int, city text, "
                       "created_at text, message text, color text, vote_count int, pin_count int, child_count int)")

    # save all the posts to the database
    cursor.executemany("INSERT OR IGNORE INTO posts VALUES(?,?,?,?,?,?,?,?,?)", posts_for_database)

    connection.commit()
