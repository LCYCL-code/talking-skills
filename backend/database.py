import aiosqlite
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "talking_skills.db")

PYRAMID_CONTENT = """金字塔原理（The Pyramid Principle）是麦肯锡咨询公司的芭芭拉·明托（Barbara Minto）在1970年代提出的一种思维和表达框架。它是一种自上而下、结论先行的结构化思维方法，广泛应用于商业写作、演讲和日常沟通中。

## 核心思想

金字塔原理的核心是：先给出结论，再陈述支撑论据。就像金字塔的结构一样，顶端是核心结论，下面是支撑这个结论的关键论点，最底层是具体的事实和数据。

## 四大基本原则

**1. 结论先行（BLUF - Bottom Line Up Front）**
- 先说最重要的结论，再解释原因
- 让听众/读者第一时间抓住核心信息
- 示例：先说"我们需要削减预算20%"，再解释3个原因

**2. 以上统下（Deductive Structure）**
- 上层观点统领下层观点
- 每个层级的内容都直接支撑上一层级的结论
- 垂直方向：WHY（为什么这样）

**3. 归类分组（MECE原则）**
- 同一层级的论点相互独立（Mutually Exclusive）
- 同一层级的论点完全穷尽（Collectively Exhaustive）
- 避免遗漏和重复
- 水平方向：HOW（如何支撑）

**4. 逻辑递进（Logical Progression）**
- 论点之间有清晰的逻辑关系
- 演绎推理：大前提→小前提→结论
- 归纳推理：多个具体案例→总结规律

## 两种主要结构

### 演绎结构（Deductive）
适合：已知结论，需要说服对方
- S（Situation 情境）：背景是什么
- C（Complication 冲突）：问题在哪里  
- Q（Question 疑问）：如何解决
- A（Answer 答案）：我的建议

### 归纳结构（Inductive）
适合：探索型分析，列举证据
- 收集多个相关事实
- 找到共同规律
- 得出归纳结论

## 实践练习方法

**练习1：一句话总结法**
读完任何一篇文章，用一句话总结主要结论。例如：
"这篇文章说明了AI将在未来5年内取代30%的重复性工作岗位。"

**练习2：金字塔重写法**
将日常表达改写为金字塔结构：
- 原版："我觉得这个项目方向不对，因为市场调研显示用户需求不在这里，而且竞争对手已经做了类似的东西，我们的技术优势也不明显。"
- 改版："**建议放弃该项目**（结论）。原因有三：①市场调研显示需求不足；②竞争对手已领先布局；③我方技术无明显优势。"

**练习3：费曼学习法结合**
用金字塔原理向一个完全不懂这个领域的人解释你刚学到的知识，检验自己是否真正理解。

## 常见错误

- 结论写在最后（"中国式"表达习惯）
- 论点之间有重叠（违反MECE）
- 论点数量过多（建议每层不超过7个）
- 论点层级混乱（细节和宏观混在同一层）

## 应用场景

- 工作汇报：先说结论和建议，再说分析过程
- 商业写作：咨询报告、分析备忘录
- 演讲展示：PPT的逻辑结构
- 邮件写作：主题行即结论
- 日常沟通：回答问题时先给答案
"""

async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                summary TEXT,
                content TEXT,
                translated_content TEXT,
                link TEXT UNIQUE,
                source TEXT,
                category TEXT DEFAULT '科技',
                content_type TEXT DEFAULT '文章',
                published_at TEXT,
                is_favorite INTEGER DEFAULT 0,
                is_read INTEGER DEFAULT 0,
                read_later INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            );

            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                original_text TEXT NOT NULL,
                ai_optimized TEXT,
                ai_direct TEXT,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (article_id) REFERENCES articles(id)
            );

            CREATE TABLE IF NOT EXISTS uploaded_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT,
                file_type TEXT,
                content TEXT,
                ai_summary TEXT,
                upload_at TEXT DEFAULT (datetime('now', 'localtime'))
            );

            CREATE TABLE IF NOT EXISTS file_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER,
                original_text TEXT NOT NULL,
                ai_optimized TEXT,
                ai_direct TEXT,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (file_id) REFERENCES uploaded_files(id)
            );

            CREATE TABLE IF NOT EXISTS hotspots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                platform TEXT,
                source TEXT,
                image_url TEXT,
                published_at TEXT,
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            );

            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hotspot_id INTEGER,
                nickname TEXT DEFAULT '匿名用户',
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (hotspot_id) REFERENCES hotspots(id)
            );

            CREATE TABLE IF NOT EXISTS feynman_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER,
                article_id INTEGER,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (file_id) REFERENCES uploaded_files(id),
                FOREIGN KEY (article_id) REFERENCES articles(id)
            );

            CREATE TABLE IF NOT EXISTS feynman_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (session_id) REFERENCES feynman_sessions(id)
            );
        """)
        await db.commit()

        # 迁移：添加列（如果不存在）
        for col_def in [
            "ALTER TABLE articles ADD COLUMN translated_content TEXT",
            "ALTER TABLE articles ADD COLUMN content_type TEXT DEFAULT '文章'",
            "ALTER TABLE articles ADD COLUMN is_read INTEGER DEFAULT 0",
            "ALTER TABLE articles ADD COLUMN read_later INTEGER DEFAULT 0",
            "ALTER TABLE comments ADD COLUMN user_id INTEGER REFERENCES users(id)",
            "ALTER TABLE comments ADD COLUMN likes INTEGER DEFAULT 0",
            "ALTER TABLE comments ADD COLUMN parent_id INTEGER REFERENCES comments(id)",
            "ALTER TABLE hotspots ADD COLUMN category TEXT DEFAULT 'today'",
        ]:
            try:
                await db.execute(col_def)
                await db.commit()
            except Exception:
                pass  # 列已存在，忽略


        # 用户自定义 RSS 源表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS custom_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                name TEXT,
                category TEXT DEFAULT '科技',
                content_type TEXT DEFAULT '文章',
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)

        # 用户表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                nickname TEXT,
                avatar_url TEXT,
                is_admin BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)

        # AI 配置表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ai_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                api_key TEXT,
                base_url TEXT,
                model_name TEXT,
                updated_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)
        await db.commit()

        cursor = await db.execute("SELECT COUNT(*) as cnt FROM uploaded_files")
        row = await cursor.fetchone()
        if row["cnt"] == 0:
            await db.execute(
                """INSERT INTO uploaded_files (title, filename, file_type, content, ai_summary, upload_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    "金字塔原理学习资料",
                    "pyramid_principle.txt",
                    "txt",
                    PYRAMID_CONTENT,
                    "金字塔原理是一种结论先行的结构化表达方法，核心是：先给出结论，再陈述支撑论据。四大原则：结论先行、以上统下、归类分组（MECE）、逻辑递进。适用于工作汇报、商业写作、演讲展示等场景，帮助表达更清晰、逻辑更严密。",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )

        # 初始化热点话题
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM hotspots")
        row = await cursor.fetchone()
        if row["cnt"] == 0:
            hotspots = [
                (
                    "2024年AI大模型年度回顾：谁赢了这场军备竞赛？",
                    "2024年是AI大模型爆发的关键年份。GPT-4、Claude 3、Gemini Ultra相继发布，国内百模大战也进入白热化阶段。智谱、百度、阿里、字节跳动纷纷推出自己的旗舰模型……",
                    "微博",
                    "科技日报",
                    None,
                    "2024-12-31",
                ),
                (
                    "年轻人为什么不爱上班了？",
                    "最近，一个关于「上班」的话题引发了广泛讨论。越来越多的年轻人表示，他们并非不想工作，而是不想「上班」——不想被固定的时间和地点束缚，不想在重复性劳动中消耗人生……",
                    "知乎",
                    "知乎热榜",
                    None,
                    "2025-01-15",
                ),
                (
                    "如何用500块钱过好一个月？真实记录",
                    "本月初立了个flag：用500块钱度过整个月。今天来分享一下我的具体规划和实操经验：早餐控制在5元以内，自己带饭，周末可以加餐……",
                    "小红书",
                    "生活记录",
                    None,
                    "2025-01-20",
                ),
                (
                    "2025年最值得期待的10款游戏盘点",
                    "2025年游戏阵容相当豪华！《黑神话：悟空》DLC确认、《GTA6》全球同步首发、《最终幻想XVII》正式公布……作为游戏爱好者，你最期待哪款？",
                    "抖音",
                    "游戏up主",
                    None,
                    "2025-01-10",
                ),
                (
                    "程序员35岁真的是坎吗？过来人亲身经历",
                    "作为一个刚过35岁的程序员，我来说说亲身经历。确实，这个年龄在求职市场上会面临更多挑战，但绝不是「进了保险箱就失业」……",
                    "知乎",
                    "知乎经验",
                    None,
                    "2025-02-01",
                ),
            ]
            await db.executemany(
                """INSERT INTO hotspots (title, content, platform, source, image_url, published_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                hotspots,
            )
        await db.commit()

        # 初始化经典辩题（category='classic'）
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM hotspots WHERE category='classic'")
        row = await cursor.fetchone()
        if row["cnt"] == 0:
            classic_debates = [
                (
                    "西红柿炒鸡蛋，到底放不放糖？",
                    "这是中国家庭餐桌上最激烈的争论之一。放糖派说：甜咸结合才是灵魂，少了糖就是失了魂。不放糖派说：放糖简直是暴殄天物，咸鲜才是正道。你家怎么做的？",
                    "经典辩题",
                    "别吵架精选",
                    None,
                    "永久有效",
                    "classic",
                ),
                (
                    "梅西和C罗，谁才是真正的足球之王？",
                    "这场争论持续了整整二十年，双方粉丝都有充足数据和荣誉支撑。梅西派：天赋、创造力、巴萨王朝。C罗派：进球数、自律、全面性。如果只能选一个，你选谁？理由呢？",
                    "经典辩题",
                    "别吵架精选",
                    None,
                    "永久有效",
                    "classic",
                ),
                (
                    "粽子到底是甜的香还是咸的香？",
                    "每年端午节，南北方必有一战。北方：放红枣、豆沙，甜粽才对。南方：猪肉、蛋黄、咸蛋，咸粽才是灵魂。还有无糖无盐纯白粽派……你站哪边？",
                    "经典辩题",
                    "别吵架精选",
                    None,
                    "永久有效",
                    "classic",
                ),
                (
                    "猫和狗，哪个更适合当宠物？",
                    "猫派：独立、不粘人、安静、优雅，养猫就是养了一个大爷。狗派：忠诚、热情、互动多，养狗是真朋友。你更偏向哪边？如果必须选一个，选什么？",
                    "经典辩题",
                    "别吵架精选",
                    None,
                    "永久有效",
                    "classic",
                ),
                (
                    "先有鸡还是先有蛋？2025年版争论",
                    "这道古老哲学题到今天依然争论不休。生物学家说：先有蛋，因为基因突变在蛋里。哲学家说：概念定义先于存在。民间说：你不吃饭，就别来烦我。你怎么看？能说清楚吗？",
                    "经典辩题",
                    "别吵架精选",
                    None,
                    "永久有效",
                    "classic",
                ),
                (
                    "早上起床：先穿上衣还是先穿裤子？",
                    "看似荒谬，实则是一道隐藏人格测试题。先穿裤子派：下半身稳定才有安全感。先穿上衣派：上半身是灵魂核心，要先保护。你的答案是什么？能给出有说服力的理由吗？",
                    "经典辩题",
                    "别吵架精选",
                    None,
                    "永久有效",
                    "classic",
                ),
                (
                    "火锅蘸料：油碟派 vs 芝麻酱派，谁才是正统？",
                    "重庆火锅圣地流行油碟+蒜泥+香菜。北京涮肉阵地坚守芝麻酱+韭菜花+腐乳。四川人说：不用油碟的都是异端。北京人说：火锅不配芝麻酱是犯罪。你选哪边？",
                    "经典辩题",
                    "别吵架精选",
                    None,
                    "永久有效",
                    "classic",
                ),
                (
                    "《哈利·波特》里，拿出魔杖是赫敏厉害，还是伏地魔厉害？",
                    "赫敏派：全书最强技能实体，几乎每次危机都靠她解决，战斗力碾压大部分成年巫师。伏地魔派：恐吓整个魔法世界二十年，打死直接对决，差距明显。你觉得谁魔法更强？",
                    "经典辩题",
                    "别吵架精选",
                    None,
                    "永久有效",
                    "classic",
                ),
            ]
            await db.executemany(
                """INSERT INTO hotspots (title, content, platform, source, image_url, published_at, category)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                classic_debates,
            )
        await db.commit()
