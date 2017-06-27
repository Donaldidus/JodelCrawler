import jodel_api
import csv


class JodelCrawlAcc(jodel_api.JodelAccount):

    # how many racks are tracked until the first one is saved and deleted
    racks = 4

    def __init__(self, city, lat, lng, racks=4, debug=False):
        super().__init__(city=city, lat=lat, lng=lng)
        self.city = city

        # create instance variables
        self.racks = racks
        self.tracked_posts = []
        self.latest_post_id = ''
        self.debug = debug

        self.authorized_tries = 0

    def fetch_new_posts(self, limit=100):
        if not self.latest_post_id:
            posts = self.get_posts_recent(skip=0, limit=limit)
        else:
            posts = self.get_posts_recent(skip=0, limit=limit, after=self.latest_post_id)

        if posts[0] == 200:
            self.authorized_tries = 0
            if posts[1]['posts']:
                self.latest_post_id = posts[1]['posts'][-1]['post_id']
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

    def drop_latest_tracked_posts(self, path):
        if self.tracked_posts:
            if len(self.tracked_posts) >= self.racks:
                # refresh post details before saving

                self._refresh_tracked_posts(index=-1)
                posts = self.tracked_posts[-1]
                # reverse list so latest post is always at the bottom of the file
                posts = reversed(posts)
                with open(path, 'a', newline='', encoding='utf-8') as file:
                    if self.debug:
                        print('saving to file')
                    writer = csv.writer(file, delimiter=';')
                    for post in posts:
                        # filter images and empty posts
                        if 'image_url' not in post.keys() and post['message'] != '':
                            # save post data to file
                            writer.writerow([post['post_id'], post['created_at'], post['message'], post['color'],
                                             post['vote_count'], post['pin_count'], post['child_count']])

                # delete the posts from memory that have been saved to disk
                self.tracked_posts.pop(-1)
