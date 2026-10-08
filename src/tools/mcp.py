import os

from strands.tools.mcp import MCPClient


def create_bronto_mcp_client() -> MCPClient | None:
    """
    Create a Bronto MCP client when configuration is available.

    Returns None when BRONTO_API_KEY is not configured.
    """

    api_key = os.getenv("BRONTO_API_KEY")

    if not api_key:
        return None

    url = os.getenv(
        "BRONTO_MCP_URL",
        "https://mcp.eu.bronto.io/mcp",
    )

    return MCPClient(
        url=url,
        headers={
            "X-BRONTO-API-KEY": api_key,
        },
        prefix="bronto",
    )
