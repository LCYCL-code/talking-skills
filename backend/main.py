from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from routers import articles, summaries, uploads, feynman, hotspots, settings, custom_sources, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Talking Skills API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origins=["*"],  # 允许所有域名访问 (为了 Netlify 部署)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router)
app.include_router(summaries.router)
app.include_router(uploads.router)
app.include_router(feynman.router)
app.include_router(hotspots.router)
app.include_router(settings.router)
app.include_router(custom_sources.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Talking Skills API 运行正常"}
