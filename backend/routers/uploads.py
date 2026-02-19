import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import aiosqlite
from database import get_db
from services import ai_service

router = APIRouter(prefix="/api/uploads", tags=["uploads"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "text/plain": "txt",
    "image/jpeg": "jpg",
    "image/png": "png",
}


@router.get("")
async def list_uploads(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM uploaded_files ORDER BY id DESC")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


@router.get("/{file_id}")
async def get_upload(file_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM uploaded_files WHERE id=?", (file_id,))
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="文件不存在")
    return dict(row)


@router.delete("/{file_id}")
async def delete_upload(file_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT file_path FROM uploaded_files WHERE id=?", (file_id,))
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="文件不存在")
    # 删除磁盘文件
    file_path = row["file_path"]
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
    # 删除关联的总结
    await db.execute("DELETE FROM file_summaries WHERE file_id=?", (file_id,))
    # 删除文件记录
    await db.execute("DELETE FROM uploaded_files WHERE id=?", (file_id,))
    await db.commit()
    return {"message": "删除成功"}


@router.post("")
async def upload_file(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: aiosqlite.Connection = Depends(get_db),
):
    # 文件大小检查（10MB）
    content_bytes = await file.read()
    if len(content_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小不能超过10MB")

    file_type = ALLOWED_TYPES.get(file.content_type, "")
    if not file_type:
        # 尝试从文件名推断
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        file_type = ext if ext in ["pdf", "docx", "pptx", "txt", "jpg", "png"] else "unknown"

    # 保存文件
    safe_name = f"{int(__import__('time').time())}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(file_path, "wb") as f:
        f.write(content_bytes)

    # 尝试提取文本内容
    text_content = ""
    try:
        if file_type == "txt":
            text_content = content_bytes.decode("utf-8", errors="ignore")
        elif file_type == "pdf":
            try:
                import pypdf
                import io
                reader = pypdf.PdfReader(io.BytesIO(content_bytes))
                text_content = "\n".join([page.extract_text() for page in reader.pages])
            except ImportError:
                print("pypdf verified not installed, skipping pdf extraction")
        elif file_type == "docx":
            try:
                import docx
                import io
                doc = docx.Document(io.BytesIO(content_bytes))
                text_content = "\n".join([para.text for para in doc.paragraphs])
            except ImportError:
                print("python-docx verified not installed, skipping docx extraction")
    except Exception as e:
        print(f"Error extracting text: {e}")
        pass

    # 生成AI摘要
    ai_summary = ""
    if text_content:
        try:
            ai_summary = await ai_service.direct_summary(text_content)
        except Exception as e:
            ai_summary = f"[摘要生成失败] {str(e)}"

    cursor = await db.execute(
        """INSERT INTO uploaded_files (title, filename, file_path, file_type, content, ai_summary)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (title, file.filename, file_path, file_type, text_content, ai_summary),
    )
    await db.commit()
    file_id = cursor.lastrowid
    return {"id": file_id, "message": "上传成功"}


class FileSummaryCreate(BaseModel):
    original_text: str

from services.moderation import check_content


@router.post("/{file_id}/summary")
async def create_file_summary(
    file_id: int,
    body: FileSummaryCreate,
    db: aiosqlite.Connection = Depends(get_db),
):
    original_text = check_content(body.original_text, max_len=2000, field_name="总结")

    cursor = await db.execute("SELECT content, ai_summary FROM uploaded_files WHERE id=?", (file_id,))
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="文件不存在")
    file_content = row["content"] or row["ai_summary"] or ""

    ai_optimized = ""
    ai_direct = ""
    try:
        ai_optimized = await ai_service.optimize_summary(file_content, original_text)
        ai_direct = await ai_service.direct_summary(file_content)
    except ValueError as e:
        ai_optimized = f"[AI功能未启用] {str(e)}"
        ai_direct = f"[AI功能未启用] {str(e)}"
    except Exception as e:
        ai_optimized = f"[AI处理失败] {str(e)}"
        ai_direct = f"[AI处理失败] {str(e)}"

    cursor = await db.execute(
        """INSERT INTO file_summaries (file_id, original_text, ai_optimized, ai_direct)
           VALUES (?, ?, ?, ?)""",
        (file_id, original_text, ai_optimized, ai_direct),
    )
    await db.commit()
    summary_id = cursor.lastrowid
    return {
        "id": summary_id,
        "original_text": original_text,
        "ai_optimized": ai_optimized,
        "ai_direct": ai_direct,
    }


@router.get("/{file_id}/summaries")
async def get_file_summaries(file_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT * FROM file_summaries WHERE file_id=? ORDER BY id DESC", (file_id,)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]
