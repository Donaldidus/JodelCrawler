# JodelCrawler

A small crawler that tracks posts from the Jodel App and saves them in a sqlite database.

## Usage
### Installation
- Install [jodel_api](https://github.com/nborrmann/jodel_api) using pip
- Clone this repo to your local machine
- Specify directories in `directories.py`
- Create accounts using `create_account.py`

The accounts are saved to disk and reused every time you run main_crawler.py.

### Crawling
- Run crawler `main_crawl.py`
- If you want you can update the posts using `refresh_data.py`

To keep traffic and load on the machine in reasonable limits only posts that have been saved in the last 20 hours will get a refresh. If you'd like to change this adjust `refresh_time_limit` property in `refresh_data.py`.

## What data is saved?
Right now only original posts are being stored (no comments).

For each post the following data is saved:
- *post_id*
- *city*
- *created_at*
- *message*
- *color*
- *vote_count*
- *pin_count*
- *child_count*

Image posts and empty posts are ignored.

There is quite some more data handed out by the Jodel servers, feel free to track those too.

## Third party packages used
- [jodel_api](https://github.com/nborrmann/jodel_api)

