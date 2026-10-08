from dotenv import load_dotenv

from src.tools.mcp import create_bronto_mcp_client


load_dotenv()

client = create_bronto_mcp_client()

if client is None:
    raise RuntimeError("BRONTO_API_KEY is not configured")

with client:
    tools = client.list_tools_sync()

    print("Connected to Bronto MCP.")
    print(f"Available tools: {len(tools)}")

    for tool in tools:
        print(f"- {tool.tool_name}")
