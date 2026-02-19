from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import aiosqlite
from database import get_db
from routers.auth import get_current_user_optional
from services.moderation import check_content

router = APIRouter(prefix="/api/hotspots", tags=["hotspots"])


@router.get("")
async def get_hotspots(platform: str = "全部", category: str = "today", db: aiosqlite.Connection = Depends(get_db)):
    if category == "classic":
        cursor = await db.execute(
            "SELECT * FROM hotspots WHERE category='classic' ORDER BY id DESC"
        )
    elif platform == "全部":
        cursor = await db.execute(
            "SELECT * FROM hotspots WHERE category='today' OR category IS NULL ORDER BY id DESC"
        )
    else:
        cursor = await db.execute(
            "SELECT * FROM hotspots WHERE (category='today' OR category IS NULL) AND platform=? ORDER BY id DESC",
            (platform,),
        )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


@router.get("/{hotspot_id}")
async def get_hotspot(hotspot_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM hotspots WHERE id=?", (hotspot_id,))
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="热点不存在")
    return dict(row)


@router.get("/{hotspot_id}/comments")
async def get_comments(hotspot_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM comments WHERE hotspot_id=? ORDER BY id DESC", (hotspot_id,)
    )
    rows = await cursor.fetchall()
    all_comments = [dict(row) for row in rows]

    # 构建树结构：顶级评论 + 子评论
    top_level = []
    replies_map = {}
    for c in all_comments:
        c["replies"] = []
        if c.get("parent_id"):
            replies_map.setdefault(c["parent_id"], []).append(c)
        else:
            top_level.append(c)

    # 把回复挂载到父评论
    for c in top_level:
        c["replies"] = replies_map.get(c["id"], [])
        # 回复按时间正序
        c["replies"].sort(key=lambda x: x["id"])

    return top_level


class CommentCreate(BaseModel):
    nickname: str = "匿名用户"
    content: str
    parent_id: int | None = None


@router.post("/{hotspot_id}/comments")
async def post_comment(
    hotspot_id: int,
    body: CommentCreate,
    db: aiosqlite.Connection = Depends(get_db),
    current_user=Depends(get_current_user_optional),
):
    content = check_content(body.content, max_len=500, field_name="评论")

    if current_user:
        nickname = current_user["nickname"]
        user_id = current_user["id"]
    else:
        nickname = body.nickname.strip() or "匿名用户"
        if len(nickname) > 20:
            raise HTTPException(status_code=400, detail="昵称不能超过20字")
        user_id = None

    # 检查 parent_id 合法性
    if body.parent_id:
        cursor = await db.execute(
            "SELECT id FROM comments WHERE id=? AND hotspot_id=?",
            (body.parent_id, hotspot_id),
        )
        if not await cursor.fetchone():
            raise HTTPException(status_code=400, detail="回复的评论不存在")

    cursor = await db.execute(
        "INSERT INTO comments (hotspot_id, nickname, content, user_id, parent_id) VALUES (?, ?, ?, ?, ?)",
        (hotspot_id, nickname, content, user_id, body.parent_id),
    )
    await db.commit()
    comment_id = cursor.lastrowid
    return {
        "id": comment_id,
        "nickname": nickname,
        "content": content,
        "parent_id": body.parent_id,
        "likes": 0,
        "message": "发表成功",
    }


@router.post("/{hotspot_id}/comments/{comment_id}/like")
async def like_comment(
    hotspot_id: int,
    comment_id: int,
    db: aiosqlite.Connection = Depends(get_db),
):
    cursor = await db.execute(
        "SELECT id, likes FROM comments WHERE id=? AND hotspot_id=?",
        (comment_id, hotspot_id),
    )
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="评论不存在")

    new_likes = (row["likes"] or 0) + 1
    await db.execute("UPDATE comments SET likes=? WHERE id=?", (new_likes, comment_id))
    await db.commit()
    return {"likes": new_likes}
