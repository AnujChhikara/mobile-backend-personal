"""MCP Server for task creation tools.

This module defines MCP-style tools that can be used with LLM function calling.
"""

import logging
import time
from typing import Any, Dict, List, Optional

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)


# MCP Tool Definitions (in OpenAI function calling format)
def get_mcp_tools() -> List[Dict[str, Any]]:
    """Get list of MCP tools available for LLM function calling."""
    return [
        {
            "type": "function",
            "function": {
                "name": "createTask",
                "description": "Creates a new task with title, description, deadline, priority, etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Task title (required)",
                        },
                        "description": {
                            "type": "string",
                            "description": "Task description (optional)",
                        },
                        "endsOn": {
                            "type": "number",
                            "description": "Deadline as Unix timestamp in seconds (optional)",
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["LOW", "MEDIUM", "HIGH", "URGENT"],
                            "description": "Task priority level (optional)",
                        },
                        "assignee": {
                            "type": "string",
                            "description": "User ID of the assignee (optional)",
                        },
                        "type": {
                            "type": "string",
                            "description": "Task type (optional)",
                        },
                    },
                    "required": ["title"],
                },
            },
        }
    ]


def validate_create_task_input(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate createTask input data.

    Args:
        data: Task data dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if not data.get("title"):
        return False, "Title is required"

    # Validate deadline if provided
    if "endsOn" in data and data["endsOn"] is not None:
        current_time = int(time.time())
        if data["endsOn"] <= current_time:
            return False, "Deadline must be in the future"

    # Validate priority if provided
    if "priority" in data and data["priority"]:
        valid_priorities = ["LOW", "MEDIUM", "HIGH", "URGENT"]
        if data["priority"] not in valid_priorities:
            return False, f"Priority must be one of: {', '.join(valid_priorities)}"

    return True, None


async def execute_create_task(
    title: str,
    description: Optional[str] = None,
    endsOn: Optional[int] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    type: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute createTask tool - calls backend API.

    Args:
        title: Task title (required)
        description: Task description
        endsOn: Deadline as Unix timestamp
        priority: Task priority (LOW/MEDIUM/HIGH/URGENT)
        assignee: User ID of assignee
        type: Task type
        token: Authentication token for backend API

    Returns:
        Dictionary with result data
    """
    settings = get_settings()

    # Validate input
    task_data = {
        "title": title,
        "description": description,
        "endsOn": endsOn,
        "priority": priority,
        "assignee": assignee,
        "type": type,
    }
    is_valid, error_msg = validate_create_task_input(task_data)
    if not is_valid:
        return {
            "success": False,
            "error": error_msg,
        }

    # Prepare request payload (remove None values)
    payload = {k: v for k, v in task_data.items() if v is not None}

    # Call backend API
    try:
        api_url = f"{settings.backend_url}/tasks"
        headers = {}
        if token:
            # Support both Bearer token and cookie format
            if token.startswith("Bearer "):
                headers["Authorization"] = token
            else:
                headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)

            if response.is_success:
                result_data = response.json() if response.content else {}
                return {
                    "success": True,
                    "message": "Task created successfully",
                    "data": result_data,
                }
            else:
                error_detail = response.text or f"HTTP {response.status_code}"
                return {
                    "success": False,
                    "error": f"Backend API error: {error_detail}",
                    "status_code": response.status_code,
                }

    except httpx.TimeoutException:
        logger.error("Timeout calling backend API")
        return {
            "success": False,
            "error": "Request timeout - backend API did not respond in time",
        }
    except Exception as e:
        logger.error(f"Error calling backend API: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"Error calling backend API: {str(e)}",
        }


async def execute_tool(tool_name: str, arguments: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
    """Execute an MCP tool by name.

    Args:
        tool_name: Name of the tool to execute
        arguments: Tool arguments
        token: Authentication token

    Returns:
        Tool execution result
    """
    if tool_name == "createTask":
        return await execute_create_task(
            title=arguments.get("title"),
            description=arguments.get("description"),
            endsOn=arguments.get("endsOn"),
            priority=arguments.get("priority"),
            assignee=arguments.get("assignee"),
            type=arguments.get("type"),
            token=token,
        )
    else:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}",
        }
