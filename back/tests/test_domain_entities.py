import unittest
from uuid import uuid4
from datetime import datetime
from back.domain.entities import Actor, Note

class TestDomainEntities(unittest.TestCase):
    def setUp(self):
        self.actor_id = uuid4()
        self.actor = Actor(
            id=self.actor_id,
            username="alice",
            preferred_username="Alice",
            public_key="RSA_PUB_KEY_CONTENT"
        )
        
        self.note_id = uuid4()
        self.note = Note(
            id=self.note_id,
            author_id=self.actor_id,
            content="Hello ActivityPub",
            published=datetime(2026, 3, 7, 12, 0, 0)
        )

    def test_actor_initialization(self):
        """Actorが正しく初期化されるか検証"""
        self.assertEqual(self.actor.id, self.actor_id)
        self.assertEqual(self.actor.username, "alice")
        self.assertEqual(self.actor.preferred_username, "Alice")
        self.assertEqual(self.actor.public_key, "RSA_PUB_KEY_CONTENT")

    def test_note_initialization(self):
        """Noteが正しく初期化されるか検証"""
        self.assertEqual(self.note.id, self.note_id)
        self.assertEqual(self.note.author_id, self.actor_id)
        self.assertEqual(self.note.content, "Hello ActivityPub")
        self.assertEqual(self.note.published, datetime(2026, 3, 7, 12, 0, 0))

    def test_note_to_create_activity(self):
        """NoteがCreateアクティビティに正しく変換されるか検証"""
        activity = self.note.to_activity(type="Create")
        
        self.assertEqual(activity["type"], "Create")
        self.assertEqual(activity["actor"], self.actor_id)
        self.assertEqual(activity["object"]["id"], self.note_id)
        self.assertEqual(activity["object"]["type"], "Note")

    def test_note_to_delete_activity(self):
        """NoteがDeleteアクティビティに正しく変換されるか検証"""
        activity = self.note.to_activity(type="Delete")
        
        self.assertEqual(activity["type"], "Delete")
        self.assertEqual(activity["actor"], self.actor_id)
        self.assertEqual(activity["object"], self.note_id)

    def test_actor_create_follow_activity(self):
        """Actorが別のActorをFollowするアクティビティを検証"""
        target_actor_id = uuid4()
        activity = self.actor.create_activity(type="Follow", object_id=target_actor_id)
        
        self.assertEqual(activity["type"], "Follow")
        self.assertEqual(activity["actor"], self.actor_id)
        self.assertEqual(activity["object"], target_actor_id)

    def test_note_to_like_activity(self):
        """Noteに対するLikeアクティビティを検証"""
        liker_id = uuid4()
        activity = self.note.to_activity(type="Like", actor_id=liker_id)
        
        self.assertEqual(activity["type"], "Like")
        self.assertEqual(activity["actor"], liker_id)
        self.assertEqual(activity["object"], self.note_id)

    def test_note_to_announce_activity(self):
        """NoteのAnnounce (Remote/Boost) アクティビティを検証"""
        announcer_id = uuid4()
        activity = self.note.to_activity(type="Announce", actor_id=announcer_id)
        
        self.assertEqual(activity["type"], "Announce")
        self.assertEqual(activity["actor"], announcer_id)
        self.assertEqual(activity["object"], self.note_id)

if __name__ == "__main__":
    unittest.main()
