"""
Console task CLI module for handling task-related interactions.
"""
from typing import List, Optional
import asyncio
from api_client import ApiClient


class TaskCLI:
    """Task CLI module for handling task-related interactions."""
    
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    async def add_task(self):
        """Add a new task via console prompts."""
        print("\n--- Add New Task ---")
        
        title = input("Enter task title: ").strip()
        if not title:
            print("Error: Title is required.")
            return

        description = input("Enter task description (optional, press Enter to skip): ").strip()
        if not description:
            description = None

        due_at_input = input("Enter due date (optional, format: YYYY-MM-DDTHH:MM:SS, press Enter to skip): ").strip()
        due_at = due_at_input if due_at_input else None

        priority_input = input("Enter priority (low/medium/high, optional, press Enter to skip): ").strip().lower()
        priority = priority_input if priority_input in ["low", "medium", "high"] else None

        tags_input = input("Enter tags separated by commas (optional, press Enter to skip): ").strip()
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else None

        try:
            task = await self.api_client.create_task(
                title=title,
                description=description,
                due_at=due_at,
                priority=priority,
                tags=tags
            )
            print(f"Task created successfully with ID: {task['id']}")
        except ValueError as e:
            print(f"Error creating task: {e}")
        except Exception as e:
            print(f"Failed to create task: {e}")

    async def list_tasks(self):
        """List tasks with filtering options."""
        print("\n--- List Tasks ---")
        print("Filter options:")
        print("1. All tasks")
        print("2. Completed tasks")
        print("3. Incomplete tasks")
        
        choice = input("Select filter (1-3, default is 1): ").strip()
        
        status_map = {"1": "all", "2": "completed", "3": "incomplete"}
        status = status_map.get(choice, "all")
        
        try:
            tasks = await self.api_client.list_tasks(status=status)
            
            if not tasks:
                print("No tasks found.")
                return
            
            print(f"\n--- {status.capitalize()} Tasks ---")
            for task in tasks:
                status_icon = "✓" if task["completed"] else "○"
                print(f"{status_icon} [{task['id']}] {task['title']}")
                if task.get('description'):
                    print(f"    Description: {task['description']}")
                if task.get('due_at'):
                    print(f"    Due: {task['due_at']}")
                if task.get('priority'):
                    print(f"    Priority: {task['priority']}")
                if task.get('tags'):
                    print(f"    Tags: {', '.join(task['tags'])}")
                print()
        except Exception as e:
            print(f"Failed to list tasks: {e}")

    async def update_task(self):
        """Update an existing task."""
        print("\n--- Update Task ---")
        task_id = input("Enter task ID to update: ").strip()
        
        if not task_id:
            print("Error: Task ID is required.")
            return

        try:
            # First, get the current task details
            current_task = await self.api_client.get_task(task_id)
            print(f"Current task: {current_task['title']}")
            
            # Get new values (or keep current if empty input)
            title = input(f"Enter new title (current: {current_task['title']}, press Enter to keep): ").strip()
            title = title if title else current_task['title']

            description = input(f"Enter new description (current: {current_task.get('description', 'None')}, press Enter to keep): ").strip()
            description = description if description else current_task.get('description')

            due_at_input = input(f"Enter new due date (current: {current_task.get('due_at', 'None')}, press Enter to keep): ").strip()
            due_at = due_at_input if due_at_input else current_task.get('due_at')

            priority_input = input(f"Enter new priority (current: {current_task.get('priority', 'None')}, press Enter to keep): ").strip().lower()
            priority = priority_input if priority_input in ["low", "medium", "high"] else current_task.get('priority')

            tags_input = input(f"Enter new tags (current: {', '.join(current_task.get('tags', []))}, press Enter to keep): ").strip()
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else current_task.get('tags')

            updated_task = await self.api_client.update_task(
                task_id=task_id,
                title=title,
                description=description,
                due_at=due_at,
                priority=priority,
                tags=tags
            )
            print(f"Task updated successfully: {updated_task['title']}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Failed to update task: {e}")

    async def toggle_task_completion(self):
        """Toggle task completion status."""
        print("\n--- Toggle Task Completion ---")
        task_id = input("Enter task ID to toggle: ").strip()
        
        if not task_id:
            print("Error: Task ID is required.")
            return

        try:
            task = await self.api_client.toggle_task_completion(task_id)
            status = "completed" if task["completed"] else "incomplete"
            print(f"Task '{task['title']}' marked as {status}.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Failed to toggle task completion: {e}")

    async def delete_task(self):
        """Delete a task."""
        print("\n--- Delete Task ---")
        task_id = input("Enter task ID to delete: ").strip()
        
        if not task_id:
            print("Error: Task ID is required.")
            return

        confirm = input(f"Are you sure you want to delete task {task_id}? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Deletion cancelled.")
            return

        try:
            result = await self.api_client.delete_task(task_id)
            print(f"Task {result['id']} deleted successfully.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Failed to delete task: {e}")