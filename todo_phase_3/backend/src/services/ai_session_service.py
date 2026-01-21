from agents import SQLiteSession
from typing import Optional
class AiSessionManager:
    def __init__(self, user_id: Optional[str] = None):
        self.user_id = user_id
        self.session = SQLiteSession(user_id, "conversations.db")
    async def get_session(self):
        return self.session
    
    async def get_session_items(self):
        session = self.session
        items = await session.get_items()
        def get_role(item):
            if isinstance(item, dict):
                return item.get("role")
            return getattr(item, "role", None)
        
        filtered_items = [i for i in items if get_role(i) in ("user", "assistant")]
        
        if len(filtered_items) > 50:
            await session.clear_session()
            await session.add_items(filtered_items[-50:])
            
        return filtered_items