import JodelCrawler
import sqlite3
import pickle
import os
import time
import datetime
import directories

main_dir = directories.main_dir
account_dir = directories.account_dir
data_base_dir = directories.data_base_dir

batch_size = 20

jodel_accounts = []
posts_for_database = []

# load all accounts from the account directory
for account_file in os.listdir(account_dir):
    if account_file.endswith('.pickle'):
        acc = pickle.load(open(account_dir + account_file, 'rb'))
        jodel_accounts.append(acc)

for account in jodel_accounts:
    if isinstance(account, JodelCrawler.JodelCrawlAcc):
        posts = account.get_posts_recent(skip=0, limit=batch_size)
        if posts[0] == 200:
            for post in posts[1]['posts']:
                if 'image_url' not in post.keys() and post['message'] != '':
                    try:
                        processed_post = [post['post_id'], int(time.time()), account.city, post['created_at'],
                                          post['message'], post['color'], post['vote_count'], post['pin_count'],
                                          post['child_count']]
                        posts_for_database.append(processed_post)
                    # sometimes a post seems not to have all relevant keys
                    # these posts are saved to a log file and not added to the database
                    except KeyError:
                        with open(directories.log_file, 'a') as file:
                            log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            file.write("{} -- KeyError while extracting jodel data \n".format(log_time))

        # in case of unauthorized error the account token has to be refreshed (see jodel_api docs for more info)
        elif posts[0] == 401:
            account.refresh_access_token()
            with open(directories.log_file, 'a') as file:
                log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write("Refreshing account token for Account {}. Error Code {} \n".format(account.city, posts[0]))
        else:
            # received any other error code, save to log file
            with open(directories.log_file, 'a') as file:
                log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write("Failed to fetch new posts. Error Code {} \n".format(posts[0]))
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
