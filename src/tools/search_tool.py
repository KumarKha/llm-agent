import json
import gzip

import urllib.error
import urllib.request
import urllib.parse

# Needed for MacOS Testing
import ssl
import certifi

# For testing
import os
from dotenv import load_dotenv

load_dotenv()


def execute_web_search(search_query: str):
    url = "https://api.search.brave.com/res/v1/llm/context"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": os.getenv("BRAVE_SEARCH_API"),
    }
    params = {
        "q": search_query,
        "extra_snippets": "true",
        "country": "US",
        "search_lang": "en",
    }
    url_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{url_params}"
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    try:
        req = urllib.request.Request(full_url, headers=headers)

        with urllib.request.urlopen(req, context=ssl_context) as response:
            raw_bytes = response.read()

            # 1. Handle decompression safely
            if response.getheader("Content-Encoding") == "gzip":
                raw_data = gzip.decompress(raw_bytes).decode("utf-8")
            else:
                raw_data = raw_bytes.decode("utf-8")

            data = json.loads(raw_data)

            # 2. FIX: Extract results from llm/context endpoint structure, with a fallback
            results = []
            if isinstance(data, dict):
                if "grounding" in data and "generic" in data["grounding"]:
                    results = data["grounding"]["generic"]
                else:
                    results = data.get("web", {}).get("results", data.get("web", []))

            if not results and isinstance(data, list):
                results = data

            if not results:
                return "Search completed, but yielded no relevant web results."

            formatted_snippets = []
            for i, item in enumerate(results[:5], 1):
                if not isinstance(item, dict):
                    continue

                title = item.get("title", "Untitled Webpage")
                url_path = item.get("url", "No URL provided")

                # 3. FIX: Handle both list-of-strings 'snippets' and standard 'snippet'
                snippet_data = item.get("snippets") or item.get("snippet") or ""
                if isinstance(snippet_data, list):
                    snippet = " | ".join(snippet_data[:3]).strip()
                else:
                    snippet = str(snippet_data).strip()

                if snippet:
                    # Protect local VRAM/context size by trimming each entry slightly
                    formatted_snippets.append(
                        f"[{i}] Title: {title} \nSource: {url_path}\nExcerpt: {snippet[:800]}"
                    )

            if not formatted_snippets:
                return "Search completed, but no readable text excerpts were returned from the web."
            return "\n".join(formatted_snippets)

    except urllib.error.HTTPError as e:
        return f"Error: Brave API returned HTTP status {e.code} - {e.reason}"
    except urllib.error.URLError as e:
        return f"Error: Failed to establish network connection. Reason: {e.reason}"
    except Exception as e:
        return f"Error: An unexpected error occurred while searching: {str(e)}"


SEARCH_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "execute_web_search",
        "description": "Searches the web for real-time information, news, schedules, live context using Brave Search.",
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "The precise web search query string containing key terms (e.g., 'Formula 1 standings 2026' or 'weather in Tokyo')",
                }
            },
            "required": ["search_query"],
        },
    },
}
