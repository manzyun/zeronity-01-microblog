import unittest
from uuid import uuid4
from datetime import datetime
from domain.entities import Actor, Note, Activity

class TestDomainEntities(unittest.TestCase):
    def setUp(self):
        self.actor_id = uuid4()
        self.actor = Actor(
            id=self.actor_id,
            username="alice",
            preferred_username="Alice",
            public_key="RSA_PUB_KEY_CONTENT",
            private_key="RSA_PRIV_KEY_CONTENT"
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
        self.assertEqual(self.actor.private_key, "RSA_PRIV_KEY_CONTENT")

    def test_note_initialization(self):
        """Noteが正しく初期化されるか検証"""
        self.assertEqual(self.note.id, self.note_id)
        self.assertEqual(self.note.author_id, self.actor_id)
        self.assertEqual(self.note.content, "Hello ActivityPub")
        self.assertEqual(self.note.published, datetime(2026, 3, 7, 12, 0, 0))

    def test_note_to_create_activity(self):
        """NoteがCreateアクティビティに正しく変換されるか検証"""
        activity = self.note.to_activity(type=Activity.CREATE)
        
        self.assertEqual(activity["type"], "Create")
        self.assertEqual(activity["actor"], self.actor_id)
        self.assertEqual(activity["object"]["id"], self.note_id)
        self.assertEqual(activity["object"]["type"], "Note")
        self.assertEqual(activity["object"]["content"], "Hello ActivityPub")

    def test_note_to_delete_activity(self):
        """NoteがDeleteアクティビティに正しく変換されるか検証"""
        activity = self.note.to_activity(type=Activity.DELETE)
        
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

    # --- Abnormal System Tests ---

    def test_actor_invalid_id_type(self):
        """ActorのIDがUUID型でない場合にTypeErrorを送出するか検証"""
        with self.assertRaises(TypeError):
            Actor(id="not-a-uuid", username="bob", preferred_username="Bob", public_key="KEY")

    def test_actor_empty_username(self):
        """Actorのusernameが空の場合にValueErrorを送出するか検証"""
        with self.assertRaises(ValueError):
            Actor(id=uuid4(), username="", preferred_username="Bob", public_key="KEY")

    def test_actor_empty_public_key(self):
        """Actorのpublic_keyが空の場合にValueErrorを送出するか検証"""
        with self.assertRaises(ValueError):
            Actor(id=uuid4(), username="bob", preferred_username="Bob", public_key="")

    def test_note_invalid_id_type(self):
        """NoteのIDがUUID型でない場合にTypeErrorを送出するか検証"""
        with self.assertRaises(TypeError):
            Note(id="not-a-uuid", author_id=uuid4(), content="Hi", published=datetime.now())

    def test_note_empty_content(self):
        """Noteのコンテンツが空の場合にValueErrorを送出するか検証"""
        with self.assertRaises(ValueError):
            Note(id=uuid4(), author_id=uuid4(), content="", published=datetime.now())

    def test_note_invalid_published_type(self):
        """Noteの公開日時がdatetime型でない場合にTypeErrorを送出するか検証"""
        with self.assertRaises(TypeError):
            Note(id=uuid4(), author_id=uuid4(), content="Hi", published="2026-03-07")

    def test_note_to_activity_invalid_type(self):
        """Note.to_activityにActivity Enum以外が渡された場合にTypeErrorを送出するか検証"""
        with self.assertRaises(TypeError):
            self.note.to_activity(type="Create")  # Should be Activity.CREATE

    def test_actor_create_activity_empty_type(self):
        """Actor.create_activityに空のタイプが渡された場合にValueErrorを送出するか検証"""
        with self.assertRaises(ValueError):
            self.actor.create_activity(type="", object_id=uuid4())

if __name__ == "__main__":
    unittest.main()
