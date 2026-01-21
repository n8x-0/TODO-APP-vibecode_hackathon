"""
Main console CLI module.
"""
import asyncio
from api_client import ApiClient
from task_cli import TaskCLI


class ConsoleCLI:
    """Main console CLI module."""
    
    def __init__(self):
        self.api_client = ApiClient()
        self.task_cli = TaskCLI(self.api_client)

    async def run(self):
        """Run the console application."""
        # First, check if the backend is reachable
        if not await self.api_client.health_check():
            print("Error: Backend API is not reachable.")
            print("Please ensure the FastAPI backend is running before starting the console.")
            return

        print("Welcome to the Todo Console Application!")
        print("Connected to backend successfully.")
        
        # Main menu loop
        while True:
            print("\n--- Main Menu ---")
            print("1. Add a new task")
            print("2. List tasks")
            print("3. Update a task")
            print("4. Toggle task completion")
            print("5. Delete a task")
            print("6. Exit")
            
            choice = input("Select an option (1-6): ").strip()
            
            if choice == "1":
                await self.task_cli.add_task()
            elif choice == "2":
                await self.task_cli.list_tasks()
            elif choice == "3":
                await self.task_cli.update_task()
            elif choice == "4":
                await self.task_cli.toggle_task_completion()
            elif choice == "5":
                await self.task_cli.delete_task()
            elif choice == "6":
                print("Goodbye!")
                await self.api_client.close()
                break
            else:
                print("Invalid option. Please select 1-6.")

    async def run_with_error_handling(self):
        """Run the console application with error handling."""
        try:
            await self.run()
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            await self.api_client.close()


# For direct execution
if __name__ == "__main__":
    console_cli = ConsoleCLI()
    asyncio.run(console_cli.run_with_error_handling())