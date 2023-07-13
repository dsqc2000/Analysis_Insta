import aiocron
import asyncio

from fastapi import FastAPI, Depends, Request

from api.router import router
from utils.collect_util import collect_util

from services.post_service import PostService

app = FastAPI(
    title="CQG endpoints for social data analysis", description="API for CQG", docs_url="/doc", version="0.0.1"
)


app.include_router(router)

post_service = PostService()


# Define the cron job to run my_service() every 60 minutes
crontab = aiocron.crontab('*/1 * * * *', func=post_service.collect_posts)



