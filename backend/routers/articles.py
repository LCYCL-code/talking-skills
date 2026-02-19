from fastapi import APIRouter, Depends
import aiosqlite
from database import get_db
from services import rss_service

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("")
async def get_articles(
    category: str = "全部",
    content_type: str = "全部",
    status: str = "全部",  # 全部/未读/已读
    db: aiosqlite.Connection = Depends(get_db)
):
    """获取文章列表，支持三维度筛选（话题分类 + 内容类型 + 阅读状态）"""
    conditions = []
    params = []
    if category != "全部":
        conditions.append("category=?")
        params.append(category)
    if content_type != "全部":
        conditions.append("content_type=?")
        params.append(content_type)
    
    if status == "未读":
        conditions.append("is_read=0")
    elif status == "已读":
        conditions.append("is_read=1")

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    cursor = await db.execute(
        f"SELECT * FROM articles {where} ORDER BY published_at DESC, id DESC LIMIT 150",
        params,
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


@router.post("/refresh")
async def refresh_articles(db: aiosqlite.Connection = Depends(get_db)):
    # 合并用户自定义来源
    cursor = await db.execute("SELECT url, name, category, content_type FROM custom_sources")
    custom_rows = await cursor.fetchall()
    extra_sources = [dict(r) for r in custom_rows]
    # extra_sources 里的 key 和 RSS_SOURCES 一致，type 字段用 content_type 代替
    for s in extra_sources:
        s["type"] = s.pop("content_type", "文章")

    articles = await rss_service.fetch_all_articles(extra_sources=extra_sources)
    added = 0
    for a in articles:
        try:
            await db.execute(
                """INSERT OR IGNORE INTO articles
                   (title, summary, content, link, source, category, content_type, published_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (a["title"], a["summary"], a["content"], a["link"],
                 a["source"], a["category"], a.get("content_type", "文章"), a["published_at"]),
            )
            added += 1
        except Exception:
            pass
    await db.commit()
    return {"message": "内容已更新", "added": added}


@router.get("/favorites")
async def get_favorites(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM articles WHERE is_favorite=1 ORDER BY id DESC"
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


@router.get("/read-later")
async def get_read_later(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM articles WHERE read_later=1 ORDER BY id DESC"
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


@router.delete("/{article_id}")
async def delete_article(article_id: int, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("DELETE FROM articles WHERE id=?", (article_id,))
    await db.commit()
    return {"ok": True}


@router.get("/{article_id}")
async def get_article(article_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM articles WHERE id=?", (article_id,))
    row = await cursor.fetchone()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="文章不存在")

    article = dict(row)
    # 自动标记已读
    await db.execute("UPDATE articles SET is_read=1 WHERE id=?", (article_id,))
    await db.commit()

    content = article.get("content") or ""
    summary = article.get("summary") or ""
    link = article.get("link") or ""

    # 若无全文（content 与 summary 相同或过短），按需抓取并缓存
    need_fetch = link and (not content or content == summary or len(content) < 300)
    if need_fetch:
        full = await rss_service.fetch_article_full_content(link)
        if full and len(full) > len(content):
            await db.execute("UPDATE articles SET content=? WHERE id=?", (full, article_id))
            await db.commit()
            article["content"] = full

    article["is_read"] = 1
    return article


@router.post("/{article_id}/read")
async def mark_read(article_id: int, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("UPDATE articles SET is_read=1 WHERE id=?", (article_id,))
    await db.commit()
    return {"is_read": True}


@router.post("/{article_id}/read-later")
async def toggle_read_later(article_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT read_later FROM articles WHERE id=?", (article_id,))
    row = await cursor.fetchone()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="文章不存在")
    new_val = 0 if row["read_later"] else 1
    await db.execute("UPDATE articles SET read_later=? WHERE id=?", (new_val, article_id))
    await db.commit()
    return {"read_later": bool(new_val)}


@router.post("/{article_id}/translate")
async def translate_article(article_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM articles WHERE id=?", (article_id,))
    row = await cursor.fetchone()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="文章不存在")

    article = dict(row)
    if article.get("translated_content"):
        return {"translated_content": article["translated_content"]}

    text = article.get("content") or article.get("summary") or ""
    from services import ai_service
    translated = await ai_service.translate_article(text)

    try:
        await db.execute(
            "UPDATE articles SET translated_content=? WHERE id=?", (translated, article_id)
        )
        await db.commit()
    except Exception:
        pass

    return {"translated_content": translated}


@router.post("/{article_id}/favorite")
async def toggle_favorite(article_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT is_favorite FROM articles WHERE id=?", (article_id,))
    row = await cursor.fetchone()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="文章不存在")
    new_val = 0 if row["is_favorite"] else 1
    await db.execute("UPDATE articles SET is_favorite=? WHERE id=?", (new_val, article_id))
    await db.commit()
    return {"is_favorite": bool(new_val)}
