from fastapi import FastAPI
from users.views import router
from posts.views import post_router
app = FastAPI()

app.include_router(router)
app.include_router(post_router)

#fast api rowert