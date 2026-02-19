from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import aiosqlite
from database import get_db
from services import ai_service

router = APIRouter(prefix="/api/feynman", tags=["feynman"])


@router.post("/sessions")
async def create_session(
    body: dict,
    db: aiosqlite.Connection = Depends(get_db),
):
    file_id = body.get("file_id")
    article_id = body.get("article_id")

    cursor = await db.execute(
        "INSERT INTO feynman_sessions (file_id, article_id) VALUES (?, ?)",
        (file_id, article_id),
    )
    await db.commit()
    session_id = cursor.lastrowid

    # AI发第一条引导消息
    first_message = "好的！让我们用费曼学习法来学习这篇内容。首先，请用你自己的话，简单告诉我这篇内容主要讲了什么？"
    await db.execute(
        "INSERT INTO feynman_messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, "assistant", first_message),
    )
    await db.commit()

    return {"session_id": session_id, "first_message": first_message}


@router.get("/sessions/{session_id}/messages")
async def get_messages(session_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM feynman_messages WHERE session_id=? ORDER BY id ASC",
        (session_id,),
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


class MessageCreate(BaseModel):
    content: str


@router.post("/sessions/{session_id}/messages")
async def send_message(
    session_id: int,
    body: MessageCreate,
    db: aiosqlite.Connection = Depends(get_db),
):
    # 获取会话信息
    cursor = await db.execute("SELECT * FROM feynman_sessions WHERE id=?", (session_id,))
    session = await cursor.fetchone()
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    # 获取文件/文章内容
    content = ""
    if session["file_id"]:
        cursor = await db.execute(
            "SELECT content, ai_summary FROM uploaded_files WHERE id=?", (session["file_id"],)
        )
        row = await cursor.fetchone()
        if row:
            content = row["content"] or row["ai_summary"] or ""
    elif session["article_id"]:
        cursor = await db.execute(
            "SELECT content, summary FROM articles WHERE id=?", (session["article_id"],)
        )
        row = await cursor.fetchone()
        if row:
            content = row["content"] or row["summary"] or ""

    # 获取历史消息
    cursor = await db.execute(
        "SELECT role, content FROM feynman_messages WHERE session_id=? ORDER BY id ASC",
        (session_id,),
    )
    history = [dict(r) for r in await cursor.fetchall()]

    # 保存用户消息
    await db.execute(
        "INSERT INTO feynman_messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, "user", body.content),
    )
    await db.commit()

    # 调用AI
    ai_reply = ""
    try:
        ai_reply = await ai_service.feynman_chat(content, history, body.content)
    except ValueError as e:
        ai_reply = f"请先配置智谱AI API Key 以启用此功能。({str(e)})"
    except Exception as e:
        ai_reply = f"AI回复失败，请重试。({str(e)})"

    await db.execute(
        "INSERT INTO feynman_messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, "assistant", ai_reply),
    )
    await db.commit()

    return {"role": "assistant", "content": ai_reply}
