from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class McpPrompt:
    name: str
    description: str
    arguments: List[Dict[str, Any]]