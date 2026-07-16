from .search_tool import SEARCH_TOOL_SCHEMA, execute_web_search


# Tool List
tools = [
    SEARCH_TOOL_SCHEMA,
]


# Tool Registry
tool_registry = {
    "execute_web_search": execute_web_search,
}

__all__ = ["tools", "tool_registry"]
