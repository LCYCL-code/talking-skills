import os
import aiosqlite
from openai import AsyncOpenAI
from dotenv import load_dotenv
from database import DB_PATH

load_dotenv()

async def get_config():
    """优先级：数据库 > 环境变量"""
    # 1. 尝试从数据库读取
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM ai_config WHERE id = 1")
            row = await cursor.fetchone()
            if row and row["api_key"]:
                return row["api_key"], row["base_url"], row["model_name"]
    except Exception:
        pass

    # 2. 回退到环境变量 (Render 等平台配置)
    api_key = os.getenv("AI_API_KEY") or os.getenv("ZHIPU_API_KEY", "")
    base_url = os.getenv("AI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
    model_name = os.getenv("AI_MODEL_NAME", "glm-4-flash")
    return api_key, base_url, model_name

async def get_client():
    api_key, base_url, _ = await get_config()
    if not api_key or api_key == "your_api_key_here":
        raise ValueError("请先在设置页配置 AI API Key")
    return AsyncOpenAI(api_key=api_key, base_url=base_url)

async def save_ai_config(api_key: str, base_url: str, model_name: str):
    """保存配置到数据库（持久化存储）"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO ai_config (id, api_key, base_url, model_name, updated_at)
            VALUES (1, ?, ?, ?, datetime('now', 'localtime'))
            ON CONFLICT(id) DO UPDATE SET
                api_key=excluded.api_key,
                base_url=excluded.base_url,
                model_name=excluded.model_name,
                updated_at=datetime('now', 'localtime')
        """, (api_key, base_url, model_name))
        await db.commit()

async def get_ai_config_status() -> dict:
    api_key, base_url, model_name = await get_config()
    
    if not api_key or api_key == "your_api_key_here":
        return {
            "configured": False, 
            "provider": "未配置",
            "base_url": "", 
            "model_name": "", 
            "masked_key": ""
        }

    masked = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "****"
    provider = "Custom / Other"
    if "deepseek" in base_url: provider = "DeepSeek"
    elif "bigmodel.cn" in base_url: provider = "智谱AI"
    elif "moonshot" in base_url: provider = "Moonshot (Kimi)"
    elif "dashscope" in base_url: provider = "阿里云 Qwen"
    elif "api.openai.com" in base_url: provider = "OpenAI"
    
    return {
        "configured": True,
        "provider": provider,
        "base_url": base_url,
        "model_name": model_name,
        "masked_key": masked
    }

# ================= 业务功能 =================

async def optimize_summary(article_content: str, user_summary: str) -> str:
    """基于金字塔原理优化用户总结"""
    client = await get_client()
    _, _, model_name = await get_config()
    
    prompt = f"""你是一位专业的表达教练，擅长金字塔原理。

用户对以下文章进行了总结，请基于金字塔原理对其总结进行优化，使其更加清晰、有条理。

## 原始文章内容：
{article_content[:3000]}

## 用户的原始总结：
{user_summary}

## 优化要求：
1. 结论先行：第一句就点明核心观点
2. 以上统下：每个论点都支撑核心结论
3. 归类分组：相关内容归为一组，不重复不遗漏
4. 逻辑递进：论点间有清晰的逻辑关系
5. 保持用户原有的理解和视角，不要大幅改写
6. 控制在200字以内

请直接输出优化后的总结，不要有多余的前缀或解释。"""

    response = await client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


async def direct_summary(article_content: str) -> str:
    """直接对文章内容按金字塔原理生成标准总结"""
    client = await get_client()
    _, _, model_name = await get_config()

    prompt = f"""你是一位专业的内容分析师，请对以下文章按照金字塔原理生成一份结构化总结。

## 文章内容：
{article_content[:3000]}

## 总结要求：
1. **核心结论**（1-2句）：文章的核心观点是什么
2. **关键论点**（2-4点）：支撑核心结论的主要论据
3. **重要细节**（可选）：关键数据、案例或补充信息

请使用**Markdown格式**组织输出，清晰呈现层次结构，总字数控制在300字以内。"""

    response = await client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
    )
    return response.choices[0].message.content.strip()


async def feynman_chat(content: str, history: list[dict], user_message: str) -> str:
    """费曼学习法对话：AI扮演导师角色"""
    client = await get_client()
    _, _, model_name = await get_config()

    system_prompt = f"""你是一位善用费曼学习法的学习导师。你的任务是帮助用户深入理解以下内容，但不是直接讲解，而是通过提问引导用户自己思考和表达。

## 你要帮助用户理解的内容：
{content[:3000]}

## 费曼学习法四步骤：
1. 选择概念：让用户用自己的话描述内容主旨
2. 简化解释：引导用户用简单语言解释复杂概念
3. 发现漏洞：针对用户理解不足的地方追问
4. 回顾复习：帮助用户形成完整的理解

## 对话规则：
- 每次只问1-2个问题，不要一次提太多问题
- 语气友好、鼓励，像朋友之间的对话 (可以使用emoji)
- 如果用户理解有偏差，温和地引导纠正
- 如果用户理解正确，给予肯定并深入追问
- 用中文交流
- 回复简洁，不超过150字"""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    response = await client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=400,
    )
    return response.choices[0].message.content.strip()


async def translate_article(text: str) -> str:
    """将英文文章翻译成中文，保留段落结构"""
    client = await get_client()
    _, _, model_name = await get_config()
    
    prompt = f"""请将以下英文内容翻译成流畅的中文。要求：
1. 保留原文段落结构，每段之间空一行
2. 专有名词（产品名、人名、公司名）保留英文
3. 技术术语翻译后可在括号里保留英文原词
4. 语言自然流畅，符合中文阅读习惯
5. 不要添加任何解释性内容，直接输出翻译结果

原文：
{text[:4000]}"""

    response = await client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
    )
    return response.choices[0].message.content.strip()
