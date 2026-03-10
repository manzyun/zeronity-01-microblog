import unittest
from uuid import uuid4
from datetime import datetime
from domain.entities import Actor, Note, Activity, Attachment, Relationship

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

    def test_note_with_attachments(self):
        """Noteに添付ファイルを含めた初期化を検証"""
        att_id = uuid4()
        att = Attachment(id=att_id, note_id=self.note_id, type="Image", url="http://example.com/img.png", mime_type="image/png")
        note = Note(id=uuid4(), author_id=self.actor_id, content="", published=datetime.now(), attachments=[att])
        self.assertEqual(len(note.attachments), 1)
        self.assertEqual(note.attachments[0].type, "Image")

    def test_note_to_create_activity_with_attachments(self):
        """添付ファイル付きNoteがCreateアクティビティに正しく変換されるか検証"""
        att_id = uuid4()
        att = Attachment(id=att_id, note_id=self.note_id, type="Image", url="http://example.com/img.png", mime_type="image/png")
        self.note = Note(id=self.note_id, author_id=self.actor_id, content="With Attachment", published=datetime.now(), attachments=[att])
        
        activity = self.note.to_activity(type=Activity.CREATE)
        self.assertEqual(activity["type"], "Create")
        self.assertEqual(len(activity["object"]["attachment"]), 1)
        self.assertEqual(activity["object"]["attachment"][0]["type"], "Image")
        self.assertEqual(activity["object"]["attachment"][0]["url"], "http://example.com/img.png")

    def test_relationship_initialization(self):
        """Relationshipが正しく初期化されるか検証"""
        rel_id = uuid4()
        follower_id = uuid4()
        following_id = uuid4()
        rel = Relationship(id=rel_id, follower_id=follower_id, following_id=following_id, created_at=datetime.now())
        self.assertEqual(rel.follower_id, follower_id)
        self.assertEqual(rel.following_id, following_id)

    # --- Abnormal System Tests ---

    def test_actor_invalid_id_type(self):
        with self.assertRaises(TypeError):
            Actor(id="not-a-uuid", username="bob", preferred_username="Bob", public_key="KEY")

    def test_note_empty_content_and_no_attachments(self):
        """コンテンツが空かつ添付ファイルもない場合にValueErrorを送出するか検証"""
        with self.assertRaises(ValueError):
            Note(id=uuid4(), author_id=uuid4(), content="", published=datetime.now(), attachments=[])

    def test_attachment_invalid_type(self):
        """不正な添付ファイルタイプ(Image/Video以外)でValueErrorを送出するか検証"""
        with self.assertRaises(ValueError):
            Attachment(id=uuid4(), note_id=uuid4(), type="Document", url="http://example.com", mime_type="application/pdf")

    def test_relationship_same_follower_following(self):
        """自分自身をフォローしようとした場合にValueErrorを送出するか検証"""
        user_id = uuid4()
        with self.assertRaises(ValueError):
            Relationship(id=uuid4(), follower_id=user_id, following_id=user_id, created_at=datetime.now())

if __name__ == "__main__":
    unittest.main()
