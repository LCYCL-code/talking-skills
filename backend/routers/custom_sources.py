from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import aiosqlite
from database import get_db

router = APIRouter(prefix="/api/custom-sources", tags=["custom_sources"])


class CustomSourceIn(BaseModel):
    url: str
    name: str = ""
    category: str = "科技"
    content_type: str = "文章"


@router.get("")
async def list_custom_sources(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM custom_sources ORDER BY created_at DESC"
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


@router.post("")
async def add_custom_source(body: CustomSourceIn, db: aiosqlite.Connection = Depends(get_db)):
    url = body.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="订阅链接不能为空")

    name = body.name.strip() or url.split("/")[2] if "/" in url else url
    try:
        await db.execute(
            """INSERT INTO custom_sources (url, name, category, content_type)
               VALUES (?, ?, ?, ?)""",
            (url, name, body.category, body.content_type),
        )
        await db.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="该链接已存在")

    cursor = await db.execute("SELECT * FROM custom_sources WHERE url=?", (url,))
    row = await cursor.fetchone()
    return dict(row)


@router.delete("/{source_id}")
async def delete_custom_source(source_id: int, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("DELETE FROM custom_sources WHERE id=?", (source_id,))
    await db.commit()
    return {"ok": True}
