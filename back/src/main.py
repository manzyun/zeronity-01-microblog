from flask import Flask, request, jsonify, session
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict, List, Optional
from domain.entities import Actor, Note, Relationship
from usecase.actor import ActorUseCase, ActorRepository, RelationshipRepository
from usecase.note import NoteUseCase, NoteRepository

app = Flask(__name__)
app.secret_key = "development-secret-key"

# --- In-Memory Repository Implementation (Mock) ---

class InMemoryActorRepository:
    def __init__(self):
        self.actors: Dict[UUID, Actor] = {}
        self.passwords: Dict[str, str] = {}
    
    def get_by_id(self, actor_id: UUID) -> Optional[Actor]:
        return self.actors.get(actor_id)
    
    def get_by_username(self, username: str) -> Optional[Actor]:
        for actor in self.actors.values():
            if actor.username == username:
                return actor
        return None
    
    def save(self, actor: Actor, password: str) -> None:
        self.actors[actor.id] = actor
        self.passwords[actor.username] = password
    
    def verify_password(self, username: str, password: str) -> bool:
        return self.passwords.get(username) == password
    
    def delete(self, actor_id: UUID) -> bool:
        if actor_id in self.actors:
            del self.actors[actor_id]
            return True
        return False

class InMemoryNoteRepository:
    def __init__(self):
        self.notes: Dict[UUID, Note] = {}
    
    def get_by_id(self, note_id: UUID) -> Optional[Note]:
        return self.notes.get(note_id)
    
    def save(self, note: Note) -> None:
        self.notes[note.id] = note
    
    def delete(self, note_id: UUID) -> bool:
        if note_id in self.notes:
            del self.notes[note_id]
            return True
        return False
    
    def get_by_author(self, author_id: UUID) -> List[Note]:
        return [n for n in self.notes.values() if n.author_id == author_id]

class InMemoryRelationshipRepository:
    def __init__(self):
        self.rels: Dict[UUID, Relationship] = {}
    
    def get_by_follower_following(self, follower_id: UUID, following_id: UUID) -> Optional[Relationship]:
        for rel in self.rels.values():
            if rel.follower_id == follower_id and rel.following_id == following_id:
                return rel
        return None
    
    def save(self, relationship: Relationship) -> None:
        self.rels[relationship.id] = relationship
    
    def delete(self, relationship_id: UUID) -> bool:
        if relationship_id in self.rels:
            del self.rels[relationship_id]
            return True
        return False

# --- Setup UseCases ---

actor_repo = InMemoryActorRepository()
note_repo = InMemoryNoteRepository()
rel_repo = InMemoryRelationshipRepository()

actor_usecase = ActorUseCase(actor_repo, rel_repo)
note_usecase = NoteUseCase(note_repo, actor_repo)

# --- Routes ---

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    try:
        actor = actor_usecase.register(data["username"], data["password"])
        return jsonify({"id": str(actor.id), "username": actor.username}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    try:
        actor = actor_usecase.login(data["username"], data["password"])
        session["user_id"] = str(actor.id)
        return jsonify({"id": str(actor.id), "username": actor.username}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@app.route("/api/notes", methods=["POST", "GET"])
def handle_notes():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = UUID(session["user_id"])
    
    if request.method == "POST":
        data = request.json
        note = note_usecase.create_note(user_id, data.get("content", ""), data.get("attachments"))
        return jsonify({"id": str(note.id), "content": note.content}), 201
    else:
        # Simple implementation: return all notes for now, or by author
        # In a real app, this would be a personalized timeline
        all_notes = []
        for note in note_repo.notes.values():
            author = actor_repo.get_by_id(note.author_id)
            all_notes.append({
                "id": str(note.id),
                "content": note.content,
                "published": note.published.isoformat(),
                "author": {
                    "username": author.username,
                    "preferred_username": author.preferred_username
                } if author else None,
                "attachments": [
                    {
                        "type": a.type,
                        "url": a.url,
                        "mime_type": a.mime_type
                    } for a in note.attachments
                ]
            })
        # Sort by published date descending
        all_notes.sort(key=lambda x: x["published"], reverse=True)
        return jsonify(all_notes), 200

@app.route("/api/actors", methods=["GET"])
def list_actors():
    actors = []
    for actor in actor_repo.actors.values():
        actors.append({
            "id": str(actor.id),
            "username": actor.username,
            "preferred_username": actor.preferred_username
        })
    return jsonify(actors), 200

@app.route("/api/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = UUID(session["user_id"])
    try:
        success = note_usecase.delete_note(UUID(note_id), user_id)
        if success:
            return "", 204
        return jsonify({"error": "Note not found"}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403

@app.route("/api/follow/<target_id>", methods=["POST"])
def follow(target_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = UUID(session["user_id"])
    try:
        rel = actor_usecase.follow(user_id, UUID(target_id))
        return jsonify({"id": str(rel.id)}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
