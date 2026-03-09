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

    def create_activity(self, type: str, object_id: Any) -> Dict[str, Any]:
        """Actorが特定のタイプのアクティビティを生成する"""
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

    def to_activity(self, type: Activity, actor_id: UUID = None) -> Dict[str, Any]:
        """NoteをActivityPub形式のアクティビティに変換する"""
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
                "type": type,
                "actor": actor,
                "object": self.id
            }
