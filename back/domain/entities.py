from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Actor:
    id: UUID
    username: str
    preferred_username: str
    public_key: str


@dataclass(frozen=True)
class Note:
    id: UUID
    author_id: UUID
    content: str
    published: datetime
