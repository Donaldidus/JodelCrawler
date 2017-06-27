import jodel_api
import csv


class JodelCrawlAcc(jodel_api.JodelAccount):

    def __init__(self, city, lat, lng, batch_size=30, debug=False):
        super().__init__(city=city, lat=lat, lng=lng)
        self.city = city

        # create instance variables
        # batch size is the amount of jodels that will be fetched at once
        self.batch_size = batch_size
        self.tracked_posts = []
        self.debug = debug

        self.authorized_tries = 0

    def fetch_new_posts(self, limit=100):
        posts = self.get_posts_recent(skip=0, limit=limit)

        if posts[0] == 200:
            self.authorized_tries = 0
            self.tracked_posts.insert(0, posts[1]['posts'])
        # catch unauthorized error and try to refresh access token + retry fetching posts
        elif posts[0] == 401:
            self.refresh_access_token()
            # break fetching new posts after 3 fails
            if self.authorized_tries < 4:
                self.authorized_tries += 1
                self.fetch_new_posts(limit=limit)
        else:
            print('Failed to fetch new posts. Error Code', posts[0])

    def _refresh_tracked_posts(self, index=0):
        if self.debug:
            print('refreshing details')
        for j, post in enumerate(self.tracked_posts[index]):
            info = self.get_post_details(post['post_id'])
            if info[0] == 200:
                self.tracked_posts[index][j] = info[1]
            else:
                print('Failed to refresh post info for post id', post['post_id'], 'Error Code:', info[0])

    def save_batch(self, path):
        # check that tracked_posts contains posts
        if self.tracked_posts:
            # refresh post details before saving
            self._refresh_tracked_posts(index=-1)
            posts = self.tracked_posts[0]
            posts = reversed(posts)
            # reverse list so latest post is always at the bottom of the file
            with open(path, 'a', newline='', encoding='utf-8') as file:
                if self.debug:
                    print('saving to file')
                writer = csv.writer(file, delimiter=';')
                reader = csv.reader(file, delimiter=';')

                # array of post_ids already saved in the file to avoid duplicates
                saved_posts = []

                for i, row in enumerate(reader):
                    if i <= self.batch_size:
                        break
                    else:
                        saved_posts.append(row[0])

                for post in posts:
                    for i, row in enumerate(reader):
                        if i <= self.batch_size:

                    # filter images and empty posts
                    if 'image_url' not in post.keys() and post['message'] != '':

                        # save post data to file
                        writer.writerow([post['post_id'], post['created_at'], post['message'], post['color'],
                                         post['vote_count'], post['pin_count'], post['child_count']])

            # delete the posts from memory that have been saved to disk
            self.tracked_posts.pop(-1)
