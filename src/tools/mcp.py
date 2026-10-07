import os

from strands.tools.mcp import MCPClient


def create_bronto_mcp_client() -> MCPClient | None:
    """
    Create a remote Bronto MCP client when configuration is available.

    Returns None when BRONTO_MCP_URL or BRONTO_API_KEY is not configured.
    """

    url = os.getenv("BRONTO_MCP_URL")
    api_key = os.getenv("BRONTO_API_KEY")

    if not url or not api_key:
        return None

    return MCPClient(
        url=url,
        headers={
            "Authorization": f"Bearer {api_key}",
        },
        prefix="bronto",
    )
