import os
import httpx
# import asyncio
# from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("serper")

serper_api_key = os.getenv("SERPER_API_KEY", "")
serper_api_base = os.getenv("SERPER_API_BASE", "")
search_type = "news"


async def search_news(topic: str):
    request_url = f"{serper_api_base}{search_type}"
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        "q": topic
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(request_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}:\n{e}")


def format_news(news_piece: dict) -> str:
    return f"""
title: {news_piece.get('title', '')}
snippet: {news_piece.get('snippet', '')}
section: {news_piece.get('section', '')}
"""


@mcp.tool()
async def get_news(topic: str) -> str:
    """Get news about a certain topic.

    Args:
        topic: description or keywords of the news to query
    """
    data = await search_news(topic)

    if not data or "news" not in data:
        return "Unable to fetch news or no news found."

    if not data["news"]:
        return "No news for this topic."

    all_news = [format_news(news_piece) for news_piece in data["news"]]
    return "\n---\n".join(all_news)


if __name__ == '__main__':
    # Initialize and run the server
    mcp.run(transport='stdio')

    # DEBUG: uncomment to check result
    # result = asyncio.run(get_news("Anthropic"))
    # print(result)
