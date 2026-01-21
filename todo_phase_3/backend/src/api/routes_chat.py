from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import os
from ..api.deps import get_current_user
from ..domain.models.user import User
from ..services.ai_service import process_chat_message
import json

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: Request,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Chat endpoint that connects to the OpenAI API to process natural language requests
    and then executes appropriate MCP tools based on the AI's analysis
    """
    # Get the current user ID from the authenticated session
    user_id = current_user.id if current_user else "unknown_user"

    # Get the user's authentication token from cookies or headers
    user_token = None
    if "access_token" in request.cookies:
        user_token = request.cookies["access_token"]
    elif "authorization" in request.headers:
        auth_header = request.headers["authorization"]
        if auth_header.startswith("Bearer "):
            user_token = auth_header[7:]  # Remove "Bearer " prefix


    # Process the message using the AI service with user authentication and conversation context
    result = await process_chat_message(chat_request.message, user_id, user_token)
    return ChatResponse(
        conversation_id=str(user_id),
        response=result["response"],
    )