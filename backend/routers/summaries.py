from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import aiosqlite
from database import get_db
from services import ai_service
from services.moderation import check_content

router = APIRouter(prefix="/api/summaries", tags=["summaries"])


class SummaryCreate(BaseModel):
    article_id: int | None = None
    original_text: str


@router.post("")
async def create_summary(body: SummaryCreate, db: aiosqlite.Connection = Depends(get_db)):
    original_text = check_content(body.original_text, max_len=2000, field_name="总结")

    article_content = ""
    if body.article_id:
        cursor = await db.execute("SELECT content, summary FROM articles WHERE id=?", (body.article_id,))
        row = await cursor.fetchone()
        if row:
            article_content = row["content"] or row["summary"] or ""

    ai_optimized = ""
    ai_direct = ""
    try:
        ai_optimized = await ai_service.optimize_summary(article_content, original_text)
        ai_direct = await ai_service.direct_summary(article_content)
    except ValueError as e:
        # API Key 未配置
        ai_optimized = f"[AI功能未启用] {str(e)}"
        ai_direct = f"[AI功能未启用] {str(e)}"
    except Exception as e:
        ai_optimized = f"[AI处理失败] {str(e)}"
        ai_direct = f"[AI处理失败] {str(e)}"

    cursor = await db.execute(
        """INSERT INTO summaries (article_id, original_text, ai_optimized, ai_direct)
           VALUES (?, ?, ?, ?)""",
        (body.article_id, original_text, ai_optimized, ai_direct),
    )
    await db.commit()
    summary_id = cursor.lastrowid
    return {
        "id": summary_id,
        "original_text": original_text,
        "ai_optimized": ai_optimized,
        "ai_direct": ai_direct,
    }


@router.get("/article/{article_id}")
async def get_summaries(article_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM summaries WHERE article_id=? ORDER BY id DESC",
        (article_id,),
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


@router.delete("/{summary_id}")
async def delete_summary(summary_id: int, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("DELETE FROM summaries WHERE id=?", (summary_id,))
    await db.commit()
    return {"message": "删除成功"}
