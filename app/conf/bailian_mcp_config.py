# 导入核心依赖：数据类、环境变量读取、路径处理
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


# 定义mcp的服务配置
# 百炼 MCP 已从旧版 SSE 协议(/sse)升级为 Streamable HTTP 协议(/mcp)
# 若旧端点不可用，需在百炼 MCP 广场「取消开通」再重新「立即开通」完成协议升级
@dataclass
class McpConfig:
    mcp_base_url: str
    api_key: str


# 默认使用 Streamable HTTP 端点，兼容旧版 SSE 时可通过环境变量覆盖
_MCP_BASE_URL = os.getenv("MCP_DASHSCOPE_BASE_URL")
if _MCP_BASE_URL and _MCP_BASE_URL.endswith("/sse"):
    # 自动纠正：/sse 已废弃，替换为 /mcp
    _MCP_BASE_URL = _MCP_BASE_URL.replace("/sse", "/mcp")

mcp_config = McpConfig(
    mcp_base_url=_MCP_BASE_URL,
    api_key=os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY"),
)
