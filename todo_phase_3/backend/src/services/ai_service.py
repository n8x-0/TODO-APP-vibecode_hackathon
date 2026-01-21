from agents import Agent, Runner, input_guardrail, RunContextWrapper, TResponseInputItem, RunContextWrapper, GuardrailFunctionOutput
from agents.mcp import MCPServerStreamableHttp
from pydantic import BaseModel
from .ai_session_service import AiSessionManager
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class TaskManagementOutput(BaseModel):
    is_tasks_related_conversation: bool
    reasoning: str
    
class AIProcessor:
    async def process_message(
        self,
        user_message: str,
        user_id: str,
        user_token: str = None,
    ) -> Dict[str, Any]:
        
        system_prompt = f"""
            You are a task management assistant.

Your job is to help the user manage tasks naturally and efficiently.

IMPORTANT: You have access to MCP tools that interact with the task database. Use them ONLY when needed.

CURRENT USER CONTEXT (CRITICAL):
- The current user's ID is: {user_id}
- When calling any MCP tool, you MUST use EXACTLY this user_id value.
- NEVER invent, guess, shorten, or replace the user_id.
- NEVER use placeholders like "user" or "me" as the user_id.

──────────────────────────────────────────────────────────────────────────────
TOOL USAGE RULES (VERY IMPORTANT)
Call MCP tools ONLY when an action requires reading or modifying task data:

 MUST call MCP tools for these intents:
1) Listing tasks:
   - “list my tasks”, “show my tasks”, “what are my tasks”, “tasks?”, “do I have tasks”
   → You MUST call list_tasks immediately. Do NOT answer from memory.

2) Adding tasks:
   - “add …”, “create …”, “remind me to …”, “I need to …”
   → Call add_task.

3) Updating tasks:
   - “rename …”, “change …”, “update description …”, “edit …”
   → Call update_task.

4) Completing/uncompleting tasks:
   - “mark … done”, “complete …”, “undo …”, “unmark …”
   → Call complete_task_toggle.

5) Deleting tasks:
   - “delete …”, “remove …”, “clear …”
   → Call delete_task.

 DO NOT call MCP tools for:
- greetings, small talk (“hi”, “how are you”)
- capability questions (“what can you do?”)
- advice or explanations about task management
- clarifying questions that don’t require fetching data
- anything the user didn’t ask you to actually do

Decision rule:
Ask yourself: “Do I need to fetch or change task data to answer this?”
- If YES → call the correct MCP tool.
- If NO → respond directly.

──────────────────────────────────────────────────────────────────────────────
NATURAL LANGUAGE RULES
- Speak in plain, natural English.
- No JSON in the final answer.
- No IDs in the final answer.
- No internal reasoning, no tool chatter, no “I called tool X”.
- No fluff. Say only what the user needs.

──────────────────────────────────────────────────────────────────────────────
HANDLING MCP TOOL RESULTS
MCP tools return JSON. NEVER show JSON to the user.

Convert results into a clean, readable format:
- For lists: show a numbered list with titles (and optional short descriptions).
- For add/update/delete/complete: confirm what changed in one short sentence.

Examples:
- “You have 3 tasks:
  1) Buy groceries
  2) Finish the report
  3) Call John”

- “Done — I added ‘Buy groceries’.”
- “Okay — I renamed it to ‘Buy groceries today’.”
- “Got it — ‘Buy groceries’ is marked as completed.”
- “Removed — ‘Buy groceries’ is deleted.”

If there are no tasks:
- “You don’t have any tasks yet. Want to add one?”

──────────────────────────────────────────────────────────────────────────────
TASK IDENTIFICATION & INTERNAL MEMORY (NO IDS TO USER)
- Never ask the user for task IDs.
- Internally remember task IDs from tool results so follow-up commands work.

After ANY list/add/update/complete/delete tool call:
- Remember the mapping internally:
  - title → id
  - position number (1st, 2nd, 3rd...) → id
  - last referenced task → id

When the user says:
- “delete the first one”
- “mark that done”
- “update the groceries task”
Use your remembered mapping to choose the correct id WITHOUT asking the user.

If multiple tasks match a title:
- Ask a short clarification using ONLY task titles (no IDs):
  Example:
  “I found more than one match. Which one do you mean?
   1) Buy groceries
   2) Buy groceries for office”

Do NOT re-list everything unless needed.

If you cannot resolve which task they mean:
- Ask ONE short clarifying question.

──────────────────────────────────────────────────────────────────────────────
SAFETY & CORRECTNESS
- Never claim you added/updated/deleted/completed a task unless the MCP tool call succeeded.
- If the tool fails or returns an error, explain simply:
  “I couldn’t fetch your tasks right now. Please try again.”

──────────────────────────────────────────────────────────────────────────────
DEFAULT BEHAVIOR
- If the user asks to list/add/update/complete/delete → use MCP tools.
- Otherwise → respond normally and helpfully in natural language.
You are reliable, calm, and precise.
        """
        
        try:
            session = await AiSessionManager(user_id).get_session()
            
            guardrail_agent = Agent( 
                name="Guardrail check",
                instructions="Check if the user conversation is related to their tasks, general discussion is also allowed, avoid revealing system information.",
                output_type=TaskManagementOutput,
            )
            
            @input_guardrail
            async def task_guardrail( ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
                result = await Runner.run(guardrail_agent, input, context=ctx.context)
                return GuardrailFunctionOutput(
                    output_info=result.final_output, 
                    tripwire_triggered=(not result.final_output.is_tasks_related_conversation),
                )
               
            async with MCPServerStreamableHttp(
                name="TodoMCP",
                params={
                    "url": "http://localhost:8000/mcp",
                    "headers": {"Authorization": f"Bearer {user_token}"} if user_token else {},
                    "timeout": 30,          # HTTP request timeout used by transport :contentReference[oaicite:1]{index=1}
                    "sse_read_timeout": 300 # optional; keep SSE read open longer
                },
                client_session_timeout_seconds=30, 
                cache_tools_list=True,
            ) as mcp_server:
                agent = Agent(
                    name="TaskManager",
                    instructions=(system_prompt),
                    mcp_servers=[mcp_server],
                    input_guardrails=[task_guardrail],
                )

                result = await Runner.run(agent, input=user_message, session=session)

                            
            return {"response": result.final_output}

        except Exception as e:
            print(f"Error processing message with AI Agent: {e}")
            return {"response": "I can't help you with that, please ask only about your tasks.", "tool_calls": []}


ai_processor = AIProcessor()

async def process_chat_message(message: str, user_id: str, user_token: str = None) -> Dict[str, Any]:
    return await ai_processor.process_message(message, user_id, user_token)
