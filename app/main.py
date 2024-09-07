from fastapi import FastAPI
from .database import engine
from . import models
from .routers import user, post, authentication, vote

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(vote.router)

models.Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
    return {'message': 'hello world!!!'}
