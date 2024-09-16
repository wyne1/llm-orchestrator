from collections import defaultdict

class ConversationManager:
    def __init__(self):
        self.conversations = defaultdict(list)

    def get_conversation(self, session_id: str):
        return self.conversations[session_id]

    def add_message(self, session_id: str, role: str, content: str):
        self.conversations[session_id].append({"role": role, "content": content})

    def clear_conversation(self, session_id: str):
        self.conversations.pop(session_id, None)