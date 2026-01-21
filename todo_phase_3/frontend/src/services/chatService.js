// chatService.js - Service for handling chat interactions with the backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const sendMessage = async (message, conversationId = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      }),
      credentials: 'include' // This ensures cookies are sent with the request
    });

    if (!response.ok) {
      throw new Error(`Chat API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};