import json
from pathlib import Path
from datetime import datetime
from typing import List
from uuid import uuid4
from llama_index.core.base.llms.types import MessageRole, ChatMessage
from logger import rich_logger


class CustomMemory:
    def __init__(self):
        self.messages: List[dict] = []
        self.session_id = str(uuid4())
        self.session_dir = self._setup_session_directory()
        rich_logger.info(f"New session started with ID: {self.session_id}")

    def _setup_session_directory(self) -> Path:
        """Setup session directory structure"""
        base_dir = Path(__file__).parent.parent
        sessions_dir = base_dir / "history" / "sessions"
        
        if not sessions_dir.exists():
            sessions_dir.mkdir(parents=True)
            rich_logger.info("Created sessions directory")

        session_dir = sessions_dir / self.session_id
        session_dir.mkdir()
        return session_dir

    def _message_to_dict(self, role: MessageRole, content: str) -> dict:
        """Convert message to JSON serializable dictionary"""
        return {
            "role": role.value,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

    def _save_messages(self) -> None:
        """Save messages to JSON file"""
        try:
            messages_file = self.session_dir / "messages.json"
            messages_file.write_text(
                json.dumps(self.messages, indent=4, ensure_ascii=False),
                encoding="utf-8"
            )
        except Exception as e:
            rich_logger.error(f"Error saving messages: {str(e)}")

    async def add_message(self, message: ChatMessage):
        """Add a message to the conversation history"""
        message_dict = self._message_to_dict(message.role, str(message.content))
        self.messages.append(message_dict)
        self._save_messages()

    async def get_history(self) -> List[dict]:
        """Get the conversation history"""
        return self.messages

    async def load_from_thread(self, steps: List[dict]) -> None:
        """Load history from thread steps"""
        for step in steps:
            if step.get("output"):
                message = self._message_to_dict(MessageRole.ASSISTANT, str(step["output"]))
                self.messages.append(message)
            if step.get("input"):
                message = self._message_to_dict(MessageRole.USER, str(step["input"]))
                self.messages.append(message)
        
        self._save_messages()
        rich_logger.info(f"Loaded {len(steps)} messages from thread to session {self.session_id}")

    @staticmethod
    def list_sessions() -> List[str]:
        """List all available session IDs"""
        base_dir = Path(__file__).parent.parent
        sessions_dir = base_dir / "history" / "sessions"
        
        if not sessions_dir.exists():
            return []
        
        return [session.name for session in sessions_dir.iterdir()]