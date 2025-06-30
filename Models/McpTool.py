from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class McpTool:
    name: str
    description: str
    input_schema: Dict[str, Any]