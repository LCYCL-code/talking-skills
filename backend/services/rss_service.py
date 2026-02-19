import feedparser
import asyncio
from datetime import datetime
from config import RSS_SOURCES
import time


def _parse_date(entry) -> str:
    """从RSS entry解析发布日期"""
    for field in ("published_parsed", "updated_parsed", "created_parsed"):
        val = getattr(entry, field, None)
        if val:
            try:
                return datetime(*val[:6]).strftime("%Y-%m-%d")
            except Exception:
                pass
    return datetime.now().strftime("%Y-%m-%d")


def _fetch_feed(source: dict) -> list[dict]:
    """同步获取单个RSS源的文章（feedparser是同步的）"""
    articles = []
    try:
        feed = feedparser.parse(source["url"])
        entries = feed.entries[:5]  # 每源最多5篇
        for entry in entries:
            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()
            if not title or not link:
                continue
            summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
            # 清理HTML标签（简单处理）
            import re
            summary = re.sub(r"<[^>]+>", "", summary).strip()
            summary = summary[:500] if summary else ""

            articles.append({
                "title": title,
                "summary": summary,
                "content": summary,
                "link": link,
                "source": source["name"],
                "category": source["category"],
                "content_type": source.get("type") or ("简讯" if len(summary) < 400 else "文章"),
                "published_at": _parse_date(entry),
            })
    except Exception as e:
        print(f"[RSS] 获取失败 {source['name']}: {e}")
    return articles


async def fetch_all_articles(extra_sources=None) -> list[dict]:
    """并发获取所有RSS源的文章（含用户自定义源）"""
    all_sources = RSS_SOURCES + (extra_sources or [])
    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(None, _fetch_feed, source)
        for source in all_sources
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_articles = []
    seen_links = set()
    for result in results:
        if isinstance(result, list):
            for article in result:
                if article["link"] not in seen_links:
                    seen_links.add(article["link"])
                    all_articles.append(article)

    # 按发布日期倒序
    all_articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)
    return all_articles


async def fetch_article_full_content(url: str) -> str:
    """按需抓取文章完整正文（httpx + 正则，无额外依赖）"""
    import httpx, re, html as html_lib

    try:
        async with httpx.AsyncClient(
            timeout=12.0,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"}
        ) as client:
            resp = await client.get(url)
            raw = resp.text

        # 删除 script / style / nav / header / footer / aside
        raw = re.sub(
            r"<(script|style|nav|header|footer|aside|noscript)[^>]*>.*?</\1>",
            "", raw, flags=re.DOTALL | re.IGNORECASE
        )
        # 提取段落
        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", raw, flags=re.DOTALL | re.IGNORECASE)
        texts = []
        for p in paragraphs:
            text = re.sub(r"<[^>]+>", "", p).strip()
            text = html_lib.unescape(text)
            text = re.sub(r"\s+", " ", text).strip()
            if len(text) > 30:
                texts.append(text)

        result = "\n\n".join(texts)
        return result if len(result) > 100 else ""
    except Exception as e:
        print(f"[RSS] 抓取全文失败 {url}: {e}")
        return ""

