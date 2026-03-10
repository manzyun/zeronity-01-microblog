from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Protocol
from domain.entities import Actor, Relationship

class ActorRepository(Protocol):
    def get_by_id(self, actor_id: UUID) -> Optional[Actor]: ...
    def get_by_username(self, username: str) -> Optional[Actor]: ...
    def save(self, actor: Actor, password: str) -> None: ...
    def verify_password(self, username: str, password: str) -> bool: ...
    def delete(self, actor_id: UUID) -> bool: ...

class RelationshipRepository(Protocol):
    def get_by_follower_following(self, follower_id: UUID, following_id: UUID) -> Optional[Relationship]: ...
    def save(self, relationship: Relationship) -> None: ...
    def delete(self, relationship_id: UUID) -> bool: ...

class ActorUseCase:
    def __init__(self, actor_repo: ActorRepository, rel_repo: RelationshipRepository):
        self.actor_repo = actor_repo
        self.rel_repo = rel_repo

    def register(self, username: str, password: str) -> Actor:
        if self.actor_repo.get_by_username(username):
            raise ValueError("User already exists")
        
        # Simple Mock Key Generation for now
        public_key = f"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A... (mock for {username})"
        private_key = f"MIIEvAIBADANBgkqhkiG9w0BAQEFAASC... (mock for {username})"
        
        actor = Actor(
            id=uuid4(),
            username=username,
            preferred_username=username.capitalize(),
            public_key=public_key,
            private_key=private_key
        )
        self.actor_repo.save(actor, password)
        return actor

    def login(self, username: str, password: str) -> Actor:
        actor = self.actor_repo.get_by_username(username)
        if not actor or not self.actor_repo.verify_password(username, password):
            raise ValueError("Invalid username or password")
        return actor

    def follow(self, follower_id: UUID, target_id: UUID) -> Relationship:
        follower = self.actor_repo.get_by_id(follower_id)
        target = self.actor_repo.get_by_id(target_id)
        if not follower or not target:
            raise ValueError("Actor not found")
        
        existing = self.rel_repo.get_by_follower_following(follower_id, target_id)
        if existing:
            return existing
        
        relationship = Relationship(
            id=uuid4(),
            follower_id=follower_id,
            following_id=target_id,
            created_at=datetime.now()
        )
        self.rel_repo.save(relationship)
        return relationship

    def unfollow(self, follower_id: UUID, target_id: UUID) -> bool:
        rel = self.rel_repo.get_by_follower_following(follower_id, target_id)
        if rel:
            return self.rel_repo.delete(rel.id)
        return False

    def delete_actor(self, actor_id: UUID) -> bool:
        return self.actor_repo.delete(actor_id)
