from fastapi import FastAPI
from database import engine
import models

# 创建所有表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API", version="1.0.0")

# 导入路由
from api import comment_router, users_router, posts_router, auth_router, tags_router, likes_router

# 注册路由
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(tags_router)
app.include_router(comment_router)
app.include_router(likes_router)

@app.get("/")
async def read_root():
    return {"message": "Hello World", "docs": "/docs"}
