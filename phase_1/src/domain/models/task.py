"""
Task domain model representing a single todo item within the system.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    """
    Represents a single todo item within the system.
    """
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    due_at: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None

    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat() + "Z"
        if self.updated_at is None:
            self.updated_at = datetime.utcnow().isoformat() + "Z"
        if self.tags is None:
            self.tags = []