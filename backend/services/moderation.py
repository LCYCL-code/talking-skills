"""内容审核服务：屏蔽词检查 + 输入长度校验"""

from fastapi import HTTPException

# 基础屏蔽词列表（可按需扩展）
BLOCK_WORDS = [
    "傻逼", "操你", "你妈的", "草泥马", "妈的", "去死",
    "白痴", "废物", "垃圾", "滚蛋", "混蛋", "王八蛋",
    "fuck", "shit", "bitch", "asshole", "dick",
]


def check_content(text: str, max_len: int = 500, field_name: str = "内容") -> str:
    """
    校验内容合法性，返回清理后的文本。
    不合法则抛出 HTTPException。
    """
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail=f"{field_name}不能为空")
    if len(text) > max_len:
        raise HTTPException(status_code=400, detail=f"{field_name}不能超过{max_len}字")

    text_lower = text.lower()
    for word in BLOCK_WORDS:
        if word.lower() in text_lower:
            raise HTTPException(status_code=400, detail=f"{field_name}包含违禁词，请修改后重试")

    return text
