"""
Console API client for communicating with the backend API.
"""
import httpx
from typing import List, Optional, Dict, Any


class ApiClient:
    """API client for the console application."""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def health_check(self) -> bool:
        """Check if the backend API is reachable."""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False

    async def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        due_at: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a new task via API."""
        try:
            response = await self.client.post(
                f"{self.base_url}/tasks",
                json={
                    "title": title,
                    "description": description,
                    "due_at": due_at,
                    "priority": priority,
                    "tags": tags
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise ValueError(f"Validation error: {e.response.json().get('detail', 'Unknown error')}")
            else:
                raise Exception(f"Failed to create task: {e.response.status_code}")

    async def list_tasks(self, status: str = "all") -> List[Dict[str, Any]]:
        """List tasks via API with optional status filter."""
        try:
            response = await self.client.get(f"{self.base_url}/tasks", params={"status": status})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Failed to list tasks: {e.response.status_code}")

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get a single task by ID via API."""
        try:
            response = await self.client.get(f"{self.base_url}/tasks/{task_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Task with ID {task_id} not found")
            else:
                raise Exception(f"Failed to get task: {e.response.status_code}")

    async def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_at: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Update an existing task via API."""
        try:
            payload = {}
            if title is not None:
                payload["title"] = title
            if description is not None:
                payload["description"] = description
            if due_at is not None:
                payload["due_at"] = due_at
            if priority is not None:
                payload["priority"] = priority
            if tags is not None:
                payload["tags"] = tags

            response = await self.client.patch(f"{self.base_url}/tasks/{task_id}", json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise ValueError(f"Validation error: {e.response.json().get('detail', 'Unknown error')}")
            elif e.response.status_code == 404:
                raise ValueError(f"Task with ID {task_id} not found")
            else:
                raise Exception(f"Failed to update task: {e.response.status_code}")

    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task via API."""
        try:
            response = await self.client.delete(f"{self.base_url}/tasks/{task_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Task with ID {task_id} not found")
            else:
                raise Exception(f"Failed to delete task: {e.response.status_code}")

    async def toggle_task_completion(self, task_id: str) -> Dict[str, Any]:
        """Toggle task completion status via API."""
        try:
            response = await self.client.post(f"{self.base_url}/tasks/{task_id}/toggle")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Task with ID {task_id} not found")
            else:
                raise Exception(f"Failed to toggle task completion: {e.response.status_code}")

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()