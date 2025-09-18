from azure.cosmos.aio import CosmosClient
from semantic_kernel.contents import ChatHistory 
from datetime import datetime
import uuid
import os

from dotenv import load_dotenv


load_dotenv(override=True)

from enum import Enum

class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"



class CosmosChatHistoryStore:
    def __init__(self, limit=500):
        self._url = os.getenv("COSMOSDB_ENDPOINT")
        self._key =  os.getenv("COSMOSDB_KEY")
        self._db_name = os.getenv("COSMOSDB_DATABASE")
        self._container_name = os.getenv("COSMOSDB_HISTORY_CONTAINER")
        self._limit = limit

        self._client = CosmosClient(self._url, credential=self._key)
        self._container = self._client.get_database_client(self._db_name).get_container_client(self._container_name)

    async def load(self, session_id: str) -> ChatHistory:
        chat_history = ChatHistory()
        query = "SELECT * FROM c WHERE c.sessionid = @sid"
        params = [{"name": "@sid", "value": session_id}]
        results = self._container.query_items(query, parameters=params)

        async for item in results:
            role = item.get("role")
            if role == "user":
                chat_history.add_user_message(item["message"])
            elif role == "assistant":
                chat_history.add_assistant_message(item["message"])
            elif role == "system":
                chat_history.add_system_message(item["message"])
            elif role == "tool":
                chat_history.add_tool_message(item["message"])
        return chat_history

    async def add_message(
        self,
        history: ChatHistory,
        session_id: str,
        role: ChatRole,
        content: str,
        tool_call_id: str = None,
        function_name: str = None,
        
    ):
        

        # Update ChatHistory based on role
        if role == ChatRole.USER:
            history.add_user_message(content)
        elif role == ChatRole.ASSISTANT:
            history.add_assistant_message(content)
        elif role == ChatRole.SYSTEM:
            history.add_system_message(content)
        elif role == ChatRole.TOOL:
            history.add_tool_message(content, tool_call_id=tool_call_id,function_name=function_name)
        else:
            raise ValueError(f"Unknown role: {role}")

        # Persist to Cosmos
        item = {
            "id": str(uuid.uuid4()),
            "sessionid": session_id,
            "message": content,
            "role": role.value,  # store as string
            "tool_call_id": tool_call_id,
            "function_name": function_name,
            "Timestamp": datetime.utcnow().isoformat()
        }
        await self._container.create_item(item)
       