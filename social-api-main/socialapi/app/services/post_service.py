
from typing import Any, Dict, List
from typing import Type
from services.base import CRUDBase
from db import db
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.collect_util import CollectUtil
posts_collection = db.get_collection('insta-posts')


class PostService(CRUDBase):
    def __init__(self):
        super().__init__(posts_collection)
        # self.collected_posts = CollectService().collect_data()

    async def create(self, data: dict) -> dict:
        post_added = await super().create(data)
        return post_added

    async def get(self, post_link: str) -> dict:
        query = {'post_link': post_link}
        post = await posts_collection.find(query)
        return post

    async def update(self, data: dict):
        query = {'post_link': data['post_link']}
        scrape_date = data['scrapes']['scrape_date']
        likes_count = data['scrapes']['likes_count']
        comments_count = data['scrapes']['comments_count']
        comments = data['comments']
        update = {'$addToSet': {'scrapes': {'scrape_date': scrape_date,
                                            'likes_count': likes_count, 'comments_count': comments_count}}, '$set': {'comments': comments}}
        result = await posts_collection.update_one(query, update)
        return result

    async def collect_posts(self):
        collect_util = CollectUtil()
        row, column = 1,1
        posts_count = collect_util.posts_count()
        for i in range(posts_count):
            post = collect_util.collect_data(row, column)
            post_db = await self.get(post_link=post['post_link'])
            if post_db==None:
                await self.create(post)
            else:
                await self.update(post)
            row = int(i/3) + 1
            column = (i%3) +1

    async def track_engagement(self, post_link: str):
        post = self.get(post_link)
        scrapes = []
        scrapes.append({'scrape_date': post['added_date'],
                        'likes_count': post['likes_count'],
                        'comments_count': post['comments_count']})
        scrapes.append(post['scrapes'])
        track = []
        for i in range(len(scrapes)-1):

            likes_increase = scrapes[i+1]['likes_count'] - \
                scrapes[i]['likes_count']
            comments_increase = scrapes[i+1]['comments_count'] - \
                scrapes[i]['comments_count']
            track.append({'likes_increase': likes_increase,
                          'comments_increase': comments_increase})
        return track


posts_service = PostService()
