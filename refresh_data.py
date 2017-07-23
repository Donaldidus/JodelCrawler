import jodel_api
import sqlite3
import time
import datetime
import directories
import os
import pickle
import directories

for account_file in os.listdir(directories.account_dir):
    if account_file.endswith('.pickle'):
        account = pickle.load(open(directories.account_dir + account_file, 'rb'))
        break

# refreshing takes quite some time that's why it is wise to focus on recent data
# the time from that on the details get refreshed
refresh_time_limit = int(time.time()) - 24 * 60 * 60

# total number of posts that are staged for refreshing
total_refresh_attempts = 0
# total number of posts where refreshing failed (e.g. post got deleted by user)
failed_refresh_attempts = 0

connection = sqlite3.connect(directories.data_base_dir)

with connection:
    cursor = connection.cursor()

    cursor.execute("SELECT post_id FROM posts WHERE fetched_at>?", (refresh_time_limit,))

    rows_for_refresh = cursor.fetchall()

    # will look like this: [[post_id, vote_count, pin_count, child_count], ...]
    refreshed_data = []

    for row in rows_for_refresh:
        total_refresh_attempts += 1
        # fetch details from the jodel servers
        details = account.get_post_details(post_id=row[0])
        if details[0] == 200:
            # extract details and add to refresh data
            refreshed_data.append([row[0], details[1]['vote_count'], details[1]['pin_count'],
                                   details[1]['child_count']])
        else:
            failed_refresh_attempts += 1

    cursor.executemany("UPDATE posts SET vote_count=? AND pin_count=? AND child_count=? WHERE post_id=?",
                       refreshed_data)

    connection.commit()

# saving some stats to the log file for better tracking
with open(directories.log_file, 'a') as file:
    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_refreshes = 'total refreshed posts ' + str(total_refresh_attempts)
    failed_refreshes = 'total failed refresh attempts ' + str(failed_refresh_attempts)
    file.write("{} -- {} -- {}".format(log_time, all_refreshes, failed_refreshes) + os.linesep)
