from fastapi import FastAPI
import models
from database import engine
from routers import post, user, authentication


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authentication.authentication_router)
app.include_router(post.posts_router)
app.include_router(user.users_router)

@app.get("/")
def root():
    return {"Data" : "API Development in FASTAPI"}