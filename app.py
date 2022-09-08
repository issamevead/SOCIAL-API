import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.routers.unsplash as unsplash_router
import src.routers.instagram as instagram_router
import src.routers.tiktok as tiktok_router
import src.routers.twitter as twitter_router
import src.routers.youtube as youtube_router

app = FastAPI(title="Social Media API", version="1.0.0")

app.include_router(unsplash_router.collections.router)
app.include_router(unsplash_router.collection.router)
app.include_router(unsplash_router.photos.router)


app.include_router(instagram_router.user.router)
app.include_router(instagram_router.post.router)
app.include_router(instagram_router.reel.router)
app.include_router(instagram_router.highlight.router)

app.include_router(twitter_router.search.router)
app.include_router(twitter_router.user.router)
app.include_router(twitter_router.tweet.router)

app.include_router(tiktok_router.search.router)
app.include_router(tiktok_router.user.router)
app.include_router(tiktok_router.video.router)

app.include_router(youtube_router.video.router)
app.include_router(youtube_router.channel.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=4040, log_level="info", reload=True)
