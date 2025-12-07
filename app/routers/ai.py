"""AI Chat router with MCP tools integration."""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, status

from app.config import get_settings
from app.database import get_conversations_collection
from app.llm_client import get_llm_response
from app.mcp_server import execute_tool, get_mcp_tools
from app.models import ChatRequest, ChatResponse, PendingAction
from app.rate_limiter import enforce_rate_limit

router = APIRouter(prefix="/ai", tags=["AI"])

logger = logging.getLogger(__name__)


def extract_token(authorization: Optional[str]) -> Optional[str]:
    """Extract token from Authorization header."""
    if not authorization:
        return None
    # Handle "Bearer token" or just "token"
    if authorization.startswith("Bearer "):
        return authorization[7:]
    return authorization


async def get_or_create_conversation(
    user_id: str, session_id: Optional[str], token: Optional[str]
) -> dict:
    """Get existing conversation or create new one.

    Args:
        user_id: User ID
        session_id: Optional existing session ID
        token: Authentication token

    Returns:
        Conversation document
    """
    collection = get_conversations_collection()

    if session_id:
        # Get existing conversation
        conversation = await collection.find_one(
            {"session_id": session_id, "user_id": user_id}
        )

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation session not found",
            )

        # Check if expired
        expires_at = conversation.get("expires_at")
        if expires_at and datetime.utcnow() > expires_at:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Conversation session expired. Please start a new conversation.",
            )

        return conversation

    # Create new conversation
    new_session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    conversation = {
        "user_id": user_id,
        "session_id": new_session_id,
        "token": token,
        "status": "active",
        "created_at": now,
        "updated_at": now,
        "expires_at": now + timedelta(minutes=10),
        "messages": [],
        "metadata": {
            "total_messages": 0,
            "total_tool_calls": 0,
            "actions_completed": 0,
        },
    }
    await collection.insert_one(conversation)
    return conversation


def build_messages_from_conversation(conversation: dict) -> list[dict]:
    """Build messages list from conversation for LLM.

    Args:
        conversation: Conversation document

    Returns:
        List of message dictionaries
    """
    messages = []
    for msg in conversation.get("messages", []):
        messages.append(
            {
                "role": msg.get("role"),
                "content": msg.get("content", ""),
            }
        )
    return messages


def requires_confirmation(tool_calls: list) -> bool:
    """Check if tool calls require user confirmation.

    Args:
        tool_calls: List of tool calls

    Returns:
        True if confirmation required
    """
    # For now, createTask always requires confirmation
    for tool_call in tool_calls:
        if tool_call.get("name") == "createTask":
            return True
    return False


def extract_pending_action(tool_calls: list) -> Optional[PendingAction]:
    """Extract pending action from tool calls.

    Args:
        tool_calls: List of tool calls

    Returns:
        PendingAction if found
    """
    for tool_call in tool_calls:
        if tool_call.get("name") == "createTask":
            return PendingAction(
                action="createTask",
                data=tool_call.get("arguments", {}),
                validation_results=None,
            )
    return None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    authorization: Optional[str] = Header(None, alias="Authorization"),
):
    """Chat endpoint with MCP tools integration.

    Maintains conversation context and handles tool calls.
    """
    settings = get_settings()

    # Extract token
    token = extract_token(authorization)

    # Enforce rate limit
    await enforce_rate_limit(request.user_id, settings.rate_limit)

    # Get or create conversation
    conversation = await get_or_create_conversation(
        request.user_id, request.session_id, token
    )

    # Add user message to conversation
    user_message = {
        "role": "user",
        "content": request.message,
        "timestamp": datetime.utcnow(),
        "message_id": f"msg_{len(conversation['messages']) + 1}",
    }
    conversation["messages"].append(user_message)

    # Build messages for LLM (include system prompt)
    llm_messages = [
        {
            "role": "system",
            "content": """You are a helpful assistant that converts user requests into structured API calls.
Handle typos and variations gracefully (e.g., "creat" = "create", "taks" = "task").
When the user wants to create a task, use the createTask function.
Always ask for confirmation before executing actions that modify data.
Be conversational and helpful.""",
        }
    ] + build_messages_from_conversation(conversation)

    # Get MCP tools
    tools = get_mcp_tools()

    try:
        # Call LLM with tools
        llm_response = await get_llm_response(llm_messages, tools)

        # Build assistant message
        assistant_message = {
            "role": "assistant",
            "content": llm_response.content,
            "timestamp": datetime.utcnow(),
            "message_id": f"msg_{len(conversation['messages']) + 2}",
            "tool_calls": [],
            "requires_confirmation": False,
        }

        # Handle tool calls
        if llm_response.tool_calls:
            assistant_message["tool_calls"] = llm_response.tool_calls
            conversation["metadata"]["total_tool_calls"] += len(llm_response.tool_calls)

            # Check if confirmation required
            if requires_confirmation(llm_response.tool_calls):
                assistant_message["requires_confirmation"] = True
                assistant_message["pending_action"] = extract_pending_action(
                    llm_response.tool_calls
                )

                # Update confirmation message
                if assistant_message["pending_action"]:
                    action_data = assistant_message["pending_action"].data
                    title = action_data.get("title", "N/A")
                    deadline = action_data.get("endsOn")
                    deadline_str = (
                        f"deadline {datetime.fromtimestamp(deadline).strftime('%B %d, %Y')}"
                        if deadline
                        else "no deadline"
                    )
                    assistant_message["content"] = (
                        f"I'll create a task '{title}' with {deadline_str}. "
                        "Should I proceed? (yes/no)"
                    )

        # Add assistant message to conversation
        conversation["messages"].append(assistant_message)

        # Update conversation in database
        conversation["updated_at"] = datetime.utcnow()
        conversation["expires_at"] = datetime.utcnow() + timedelta(
            minutes=10
        )  # Reset expiry
        conversation["metadata"]["total_messages"] = len(conversation["messages"])

        collection = get_conversations_collection()
        await collection.update_one(
            {"session_id": conversation["session_id"]},
            {"$set": conversation},
        )

        # Build response
        pending_action = None
        if assistant_message.get("requires_confirmation") and assistant_message.get(
            "pending_action"
        ):
            pending_action_dict = assistant_message["pending_action"]
            if isinstance(pending_action_dict, dict):
                pending_action = PendingAction(**pending_action_dict)
            else:
                pending_action = pending_action_dict

        return ChatResponse(
            message=assistant_message["content"],
            session_id=conversation["session_id"],
            requires_confirmation=assistant_message.get("requires_confirmation", False),
            pending_action=pending_action,
            success=True,
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}",
        )


@router.post("/chat/confirm", response_model=ChatResponse)
async def confirm_action(
    session_id: str,
    confirmed: bool,
    user_id: str,
    authorization: Optional[str] = Header(None, alias="Authorization"),
):
    """Confirm and execute a pending action.

    Args:
        session_id: Conversation session ID
        confirmed: Whether user confirmed (true/false)
        user_id: User ID
        authorization: Authorization header with token
    """
    collection = get_conversations_collection()

    # Get conversation
    conversation = await collection.find_one(
        {"session_id": session_id, "user_id": user_id}
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation session not found",
        )

    # Check for pending action
    last_message = conversation["messages"][-1] if conversation["messages"] else None
    if not last_message or not last_message.get("requires_confirmation"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No pending action to confirm",
        )

    if not confirmed:
        # User cancelled
        cancellation_message = {
            "role": "user",
            "content": "no",
            "timestamp": datetime.utcnow(),
            "message_id": f"msg_{len(conversation['messages']) + 1}",
        }
        conversation["messages"].append(cancellation_message)

        assistant_message = {
            "role": "assistant",
            "content": "Action cancelled. No changes were made.",
            "timestamp": datetime.utcnow(),
            "message_id": f"msg_{len(conversation['messages']) + 2}",
        }
        conversation["messages"].append(assistant_message)

        conversation["updated_at"] = datetime.utcnow()
        conversation["expires_at"] = datetime.utcnow() + timedelta(minutes=10)
        await collection.update_one(
            {"session_id": session_id}, {"$set": conversation}
        )

        return ChatResponse(
            message="Action cancelled. No changes were made.",
            session_id=session_id,
            requires_confirmation=False,
            pending_action=None,
            success=True,
        )

    # User confirmed - execute action
    pending_action = last_message.get("pending_action")
    if not pending_action:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No pending action found",
        )

    action_name = pending_action.get("action") if isinstance(pending_action, dict) else pending_action.action
    action_data = pending_action.get("data") if isinstance(pending_action, dict) else pending_action.data

    # Extract token
    token = extract_token(authorization) or conversation.get("token")

    # Execute tool
    result = await execute_tool(action_name, action_data, token=token)

    # Add user confirmation message
    confirmation_message = {
        "role": "user",
        "content": "yes",
        "timestamp": datetime.utcnow(),
        "message_id": f"msg_{len(conversation['messages']) + 1}",
    }
    conversation["messages"].append(confirmation_message)

    # Add result message
    if result.get("success"):
        result_message = f"✅ {result.get('message', 'Action completed successfully!')}"
        conversation["metadata"]["actions_completed"] += 1
    else:
        result_message = f"❌ Error: {result.get('error', 'Action failed')}"

    assistant_message = {
        "role": "assistant",
        "content": result_message,
        "timestamp": datetime.utcnow(),
        "message_id": f"msg_{len(conversation['messages']) + 2}",
        "action_result": result,
    }
    conversation["messages"].append(assistant_message)

    # Update conversation
    conversation["updated_at"] = datetime.utcnow()
    conversation["expires_at"] = datetime.utcnow() + timedelta(minutes=10)
    conversation["metadata"]["total_messages"] = len(conversation["messages"])
    await collection.update_one({"session_id": session_id}, {"$set": conversation})

    return ChatResponse(
        message=result_message,
        session_id=session_id,
        requires_confirmation=False,
        pending_action=None,
        success=result.get("success", False),
    )
