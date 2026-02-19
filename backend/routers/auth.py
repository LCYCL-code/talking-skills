from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from pydantic import BaseModel
import aiosqlite
from database import get_db
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])

# JWT 配置
SECRET_KEY = os.getenv("JWT_SECRET", "talking-skills-jwt-secret-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 7


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        return None


# ===== 依赖注入：获取当前用户 =====

async def get_current_user(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    """必须登录，否则 401"""
    token = request.cookies.get("auth_token")
    if not token:
        raise HTTPException(status_code=401, detail="未登录")
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    cursor = await db.execute(
        "SELECT id, email, nickname, avatar_url, is_admin FROM users WHERE id=?", (user_id,)
    )
    user = await cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return dict(user)


async def get_current_user_optional(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    """可选登录，未登录返回 None（用于匿名评论等场景）"""
    token = request.cookies.get("auth_token")
    if not token:
        return None
    user_id = decode_token(token)
    if not user_id:
        return None
    cursor = await db.execute(
        "SELECT id, email, nickname, avatar_url, is_admin FROM users WHERE id=?", (user_id,)
    )
    user = await cursor.fetchone()
    return dict(user) if user else None


# ===== API 端点 =====

class UserRegister(BaseModel):
    email: str
    password: str
    nickname: str = "User"


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(body: UserRegister, db: aiosqlite.Connection = Depends(get_db)):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="邮箱和密码必须填写")
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="密码至少6位")
    if len(body.nickname) > 20:
        raise HTTPException(status_code=400, detail="昵称不能超过20字")

    cursor = await db.execute("SELECT id FROM users WHERE email=?", (body.email,))
    if await cursor.fetchone():
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    hashed = hash_password(body.password)
    try:
        await db.execute(
            "INSERT INTO users (email, hashed_password, nickname) VALUES (?, ?, ?)",
            (body.email, hashed, body.nickname.strip() or "User"),
        )
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "注册成功，请登录"}


@router.post("/login")
async def login(body: UserLogin, response: Response, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT id, email, nickname, hashed_password FROM users WHERE email=?",
        (body.email,),
    )
    user = await cursor.fetchone()
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")

    token = create_token(user["id"])
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        max_age=86400 * TOKEN_EXPIRE_DAYS,
        samesite="lax",
    )
    return {
        "message": "登录成功",
        "user": {"id": user["id"], "email": user["email"], "nickname": user["nickname"]},
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("auth_token")
    return {"message": "已登出"}


@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return user
