from typing import Dict, List, Tuple
import time
from collections import defaultdict

class MessageManager:
    def __init__(self):
        # Pairwise chats: {chat_key: {timestamp: message}}
        self.chats: Dict[str, Dict[int, str]] = defaultdict(dict)
        # Group/forum messages: {timestamp: message}
        self.forum: Dict[int, str] = {}
        
    def _get_chat_key(self, name1: str, name2: str) -> str:
        """Generate chat key from two names in alphabetical order"""
        names = sorted([name1, name2])
        return f"{names[0]}_{names[1]}"
    
    def _get_timestamp_key(self) -> int:
        """Get truncated timestamp for message key"""
        return int(time.time())
    
    def send_private_message(self, sender: str, recipient: str, message: str) -> int:
        """Send private message between two agents"""
        chat_key = self._get_chat_key(sender, recipient)
        timestamp = self._get_timestamp_key()
        formatted_message = f"{sender}: {message}"
        
        self.chats[chat_key][timestamp] = formatted_message
        return timestamp
    
    def send_forum_message(self, sender: str, message: str) -> int:
        """Send message to public forum"""
        timestamp = self._get_timestamp_key()
        formatted_message = f"{sender}: {message}"
        
        self.forum[timestamp] = formatted_message
        return timestamp
    
    def get_private_chat_history(self, name1: str, name2: str, limit: int = None) -> List[Tuple[int, str]]:
        """Get private chat history between two agents"""
        chat_key = self._get_chat_key(name1, name2)
        messages = self.chats[chat_key]
        
        # Sort by timestamp and apply limit if specified
        sorted_messages = sorted(messages.items())
        if limit:
            sorted_messages = sorted_messages[-limit:]
            
        return sorted_messages
    
    def get_forum_history(self, limit: int = None) -> List[Tuple[int, str]]:
        """Get forum message history"""
        sorted_messages = sorted(self.forum.items())
        if limit:
            sorted_messages = sorted_messages[-limit:]
            
        return sorted_messages
    
    def get_agent_context(self, agent_name: str, limit_private: int = 10, limit_forum: int = 20) -> Dict[str, List[Tuple[int, str]]]:
        """Extract relevant context for an agent"""
        context = {
            "private_chats": {},
            "forum": self.get_forum_history(limit_forum)
        }
        
        # Get private chats involving this agent
        for chat_key, messages in self.chats.items():
            names = chat_key.split('_')
            if agent_name in names:
                other_agent = names[0] if names[1] == agent_name else names[1]
                sorted_messages = sorted(messages.items())
                if limit_private:
                    sorted_messages = sorted_messages[-limit_private:]
                context["private_chats"][other_agent] = sorted_messages
        
        return context
    
    def get_recent_interactions(self, agent_name: str, hours: int = 24) -> List[str]:
        """Get recent interactions for an agent within specified hours"""
        cutoff_time = int(time.time()) - (hours * 3600)
        interactions = []
        
        # Check private chats
        for chat_key, messages in self.chats.items():
            if agent_name in chat_key:
                for timestamp, message in messages.items():
                    if timestamp > cutoff_time:
                        interactions.append(f"Private: {message}")
        
        # Check forum messages
        for timestamp, message in self.forum.items():
            if timestamp > cutoff_time and not message.startswith(f"{agent_name}:"):
                interactions.append(f"Forum: {message}")
        
        return sorted(interactions)