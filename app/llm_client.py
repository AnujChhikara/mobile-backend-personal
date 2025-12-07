"""LLM Client for Google Gemini with function calling."""

import logging
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from app.config import get_settings

logger = logging.getLogger(__name__)


class LLMResponse:
    """Standardized LLM response format."""

    def __init__(
        self,
        content: str,
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        finish_reason: Optional[str] = None,
    ):
        self.content = content
        self.tool_calls = tool_calls or []
        self.finish_reason = finish_reason


class LLMClient:
    """LLM client for Google Gemini."""

    def __init__(self):
        self.settings = get_settings()
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Gemini client."""
        if not self.settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY not set in environment")
        genai.configure(api_key=self.settings.google_api_key)
        self.model_name = self.settings.ai_model or "gemini-1.5-flash"

    def _extract_system_message(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Extract system message from messages list."""
        for msg in messages:
            if msg.get("role") == "system":
                return msg.get("content")
        return None

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        """Get chat completion with function calling support.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: List of tool definitions for function calling

        Returns:
            LLMResponse with content and tool calls
        """
        system_prompt = self._extract_system_message(messages)
        conversation_messages = [msg for msg in messages if msg.get("role") != "system"]

        if not system_prompt:
            system_prompt = """You are a helpful assistant that converts user requests into structured API calls.
Handle typos and variations gracefully (e.g., "creat" = "create", "taks" = "task").
When the user wants to create a task, use the createTask function.
Always ask for confirmation before executing actions that modify data."""

        try:
            return await self._gemini_chat(conversation_messages, system_prompt, tools)
        except Exception as e:
            logger.error(f"Error in LLM chat completion: {e}", exc_info=True)
            raise

    async def _gemini_chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        tools: Optional[List[Dict[str, Any]]],
    ) -> LLMResponse:
        """Google Gemini chat completion."""
        model = genai.GenerativeModel(self.model_name)

        # Build prompt with system message
        full_prompt = ""
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n"

        # Convert messages to text format for Gemini
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                full_prompt += f"User: {content}\n"
            elif role == "assistant":
                full_prompt += f"Assistant: {content}\n"

        # Gemini function calling
        gemini_tools = None
        if tools:
            # Convert tools to Gemini format
            gemini_tools = []
            for tool in tools:
                if tool.get("type") == "function":
                    gemini_tools.append(
                        {
                            "function_declarations": [
                                {
                                    "name": tool["function"]["name"],
                                    "description": tool["function"]["description"],
                                    "parameters": tool["function"]["parameters"],
                                }
                            ]
                        }
                    )

        try:
            generation_config = {
                "temperature": 0.3,
            }

            if gemini_tools:
                response = model.generate_content(
                    full_prompt,
                    tools=gemini_tools,
                    generation_config=generation_config,
                )
            else:
                response = model.generate_content(
                    full_prompt,
                    generation_config=generation_config,
                )

            tool_calls = []
            text_content = ""

            # Extract text and function calls
            if response.candidates:
                candidate = response.candidates[0]
                if candidate.content:
                    for part in candidate.content.parts:
                        if hasattr(part, "text") and part.text:
                            text_content += part.text
                        elif hasattr(part, "function_call"):
                            # Convert function call arguments to dict
                            args_dict = {}
                            if hasattr(part.function_call, "args"):
                                # Gemini function_call.args is a protobuf Struct
                                # Convert to dict
                                try:
                                    from google.protobuf.json_format import MessageToDict
                                    args_dict = MessageToDict(part.function_call.args)
                                    # Remove protobuf metadata fields
                                    args_dict = {
                                        k: v
                                        for k, v in args_dict.items()
                                        if not k.startswith("@")
                                    }
                                except Exception as e:
                                    logger.warning(f"Error converting function args: {e}")
                                    # Fallback: try to access as dict
                                    try:
                                        args_dict = dict(part.function_call.args)
                                    except Exception:
                                        args_dict = {}
                            
                            tool_calls.append(
                                {
                                    "id": f"gemini_{len(tool_calls)}",
                                    "name": part.function_call.name,
                                    "arguments": args_dict,
                                }
                            )

            return LLMResponse(
                content=text_content,
                tool_calls=tool_calls,
                finish_reason="stop",
            )
        except Exception as e:
            logger.error(f"Gemini API error: {e}", exc_info=True)
            raise


async def get_llm_response(
    messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None
) -> LLMResponse:
    """Get LLM response using Gemini.

    Args:
        messages: List of message dictionaries
        tools: Optional list of tool definitions

    Returns:
        LLMResponse object
    """
    client = LLMClient()
    return await client.chat_completion(messages, tools)
