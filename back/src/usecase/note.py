from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List, Protocol, Dict
from domain.entities import Actor, Note, Attachment

class NoteRepository(Protocol):
    def get_by_id(self, note_id: UUID) -> Optional[Note]: ...
    def save(self, note: Note) -> None: ...
    def delete(self, note_id: UUID) -> bool: ...
    def get_by_author(self, author_id: UUID) -> List[Note]: ...

class ActorRepository(Protocol):
    def get_by_id(self, actor_id: UUID) -> Optional[Actor]: ...

class NoteUseCase:
    def __init__(self, note_repo: NoteRepository, actor_repo: ActorRepository):
        self.note_repo = note_repo
        self.actor_repo = actor_repo

    def create_note(self, actor_id: UUID, content: str, attachments: List[Dict] = None) -> Note:
        actor = self.actor_repo.get_by_id(actor_id)
        if not actor:
            raise ValueError("Actor not found")
        
        note_id = uuid4()
        attachments_list = []
        if attachments:
            for att_data in attachments:
                attachment = Attachment(
                    id=uuid4(),
                    note_id=note_id,
                    type=att_data["type"],
                    url=att_data["url"],
                    mime_type=att_data["mime_type"]
                )
                attachments_list.append(attachment)
        
        note = Note(
            id=note_id,
            author_id=actor_id,
            content=content,
            published=datetime.now(),
            attachments=attachments_list
        )
        self.note_repo.save(note)
        return note

    def delete_note(self, note_id: UUID, actor_id: UUID) -> bool:
        note = self.note_repo.get_by_id(note_id)
        if not note:
            return False
        
        if note.author_id != actor_id:
            raise PermissionError("Unauthorized")
        
        return self.note_repo.delete(note_id)
