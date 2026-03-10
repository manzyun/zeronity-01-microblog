from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Any, Dict, List, Optional


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
    FOLLOW = 5
    UNDO = 6
    
@dataclass(frozen=True)
class Attachment:
    id: UUID
    note_id: UUID
    type: str # "Image" or "Video"
    url: str
    mime_type: str

    def __post_init__(self):
        if not isinstance(self.id, UUID):
            raise TypeError("id must be a UUID")
        if not isinstance(self.note_id, UUID):
            raise TypeError("note_id must be a UUID")
        if self.type not in ["Image", "Video"]:
            raise ValueError("type must be Image or Video")
        if not self.url:
            raise ValueError("url cannot be empty")

@dataclass(frozen=True)
class Note:
    id: UUID
    author_id: UUID
    content: str
    published: datetime
    attachments: List[Attachment] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.id, UUID):
            raise TypeError("id must be a UUID")
        if not isinstance(self.author_id, UUID):
            raise TypeError("author_id must be a UUID")
        if not isinstance(self.published, datetime):
            raise TypeError("published must be a datetime")
        if not self.content and not self.attachments:
            raise ValueError("content cannot be empty if no attachments")

    def to_activity(self, type: Activity, actor_id: UUID = None) -> Dict[str, Any]:
        """NoteをActivityPub形式のアクティビティに変換する"""
        if not isinstance(type, Activity):
            raise TypeError("type must be an instance of Activity enum")
        
        actor = actor_id if actor_id else self.author_id
        
        if type == Activity.CREATE:
            attachments_json = []
            for att in self.attachments:
                attachments_json.append({
                    "type": att.type,
                    "url": att.url,
                    "mediaType": att.mime_type
                })
            
            return {
                "type": "Create",
                "actor": actor,
                "object": {
                    "id": self.id,
                    "type": "Note",
                    "attributedTo": self.author_id,
                    "content": self.content,
                    "published": self.published.isoformat(),
                    "attachment": attachments_json
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

@dataclass(frozen=True)
class Relationship:
    id: UUID
    follower_id: UUID
    following_id: UUID
    created_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, UUID):
            raise TypeError("id must be a UUID")
        if not isinstance(self.follower_id, UUID):
            raise TypeError("follower_id must be a UUID")
        if not isinstance(self.following_id, UUID):
            raise TypeError("following_id must be a UUID")
        if self.follower_id == self.following_id:
            raise ValueError("follower_id cannot be the same as following_id")
