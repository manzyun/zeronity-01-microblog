from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Any, Dict


@dataclass(frozen=True)
class Actor:
    id: UUID
    username: str
    preferred_username: str
    public_key: str
    private_key: str = "" # Added to support signing activities

    def __post_init__(self):
        if not isinstance(self.id, UUID):
            raise TypeError("id must be a UUID")
        if not self.username:
            raise ValueError("username cannot be empty")
        if not self.public_key:
            raise ValueError("public_key cannot be empty")

    def create_activity(self, type: str, object_id: Any) -> Dict[str, Any]:
        """Actorが特定のタイプのアクティビティを生成する"""
        if not type:
            raise ValueError("activity type cannot be empty")
        return {
            "type": type,
            "actor": self.id,
            "object": object_id
        }


class Activity(Enum):
    """Noteタイプ"""
    CREATE = 1
    DELETE = 2
    LIKE = 3
    ANNOUNCE = 4
    
@dataclass(frozen=True)
class Note:
    id: UUID
    author_id: UUID
    content: str
    published: datetime

    def __post_init__(self):
        if not isinstance(self.id, UUID):
            raise TypeError("id must be a UUID")
        if not isinstance(self.author_id, UUID):
            raise TypeError("author_id must be a UUID")
        if not isinstance(self.published, datetime):
            raise TypeError("published must be a datetime")
        if not self.content:
            raise ValueError("content cannot be empty")

    def to_activity(self, type: Activity, actor_id: UUID = None) -> Dict[str, Any]:
        """NoteをActivityPub形式のアクティビティに変換する"""
        if not isinstance(type, Activity):
            raise TypeError("type must be an instance of Activity enum")
        
        actor = actor_id if actor_id else self.author_id
        
        if type == Activity.CREATE:
            return {
                "type": "Create",
                "actor": actor,
                "object": {
                    "id": self.id,
                    "type": "Note",
                    "attributedTo": self.author_id,
                    "content": self.content,
                    "published": self.published.isoformat()
                }
            }
        elif type == Activity.DELETE:
            return {
                "type": "Delete",
                "actor": actor,
                "object": self.id
            }
        else:
            # Like, Announce etc.
            return {
                "type": type.name.capitalize(),
                "actor": actor,
                "object": self.id
            }
