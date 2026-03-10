import unittest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime
from domain.entities import Actor, Note, Activity, Attachment, Relationship
from usecase.actor import ActorUseCase
from usecase.note import NoteUseCase

class TestUseCase(unittest.TestCase):
    def setUp(self):
        self.actor_repo = MagicMock()
        self.note_repo = MagicMock()
        self.rel_repo = MagicMock()
        
        self.actor_usecase = ActorUseCase(self.actor_repo, self.rel_repo)
        self.note_usecase = NoteUseCase(self.note_repo, self.actor_repo)

    # --- Actor UseCase Tests ---

    def test_register_success(self):
        """ユーザー登録成功を検証"""
        self.actor_repo.get_by_username.return_value = None
        
        actor = self.actor_usecase.register("bob", "password123")
        
        self.assertEqual(actor.username, "bob")
        self.assertTrue(len(actor.public_key) > 0)
        self.actor_repo.save.assert_called_once()

    def test_register_duplicate_username(self):
        """重複したユーザー名での登録失敗を検証"""
        self.actor_repo.get_by_username.return_value = MagicMock(spec=Actor)
        
        with self.assertRaises(ValueError):
            self.actor_usecase.register("bob", "password123")

    def test_login_success(self):
        """ログイン成功を検証"""
        actor_id = uuid4()
        mock_actor = Actor(id=actor_id, username="bob", preferred_username="Bob", public_key="PUB")
        self.actor_repo.get_by_username.return_value = mock_actor
        self.actor_repo.verify_password.return_value = True
        
        actor = self.actor_usecase.login("bob", "password123")
        self.assertEqual(actor.id, actor_id)

    def test_login_failure(self):
        """ログイン失敗(パスワード不一致)を検証"""
        self.actor_repo.get_by_username.return_value = MagicMock(spec=Actor)
        self.actor_repo.verify_password.return_value = False
        
        with self.assertRaises(ValueError):
            self.actor_usecase.login("bob", "wrongpass")

    def test_follow_success(self):
        """フォロー成功を検証"""
        follower_id = uuid4()
        target_id = uuid4()
        self.actor_repo.get_by_id.side_effect = [MagicMock(spec=Actor), MagicMock(spec=Actor)]
        self.rel_repo.get_by_follower_following.return_value = None
        
        rel = self.actor_usecase.follow(follower_id, target_id)
        self.assertEqual(rel.follower_id, follower_id)
        self.assertEqual(rel.following_id, target_id)
        self.rel_repo.save.assert_called_once()

    # --- Note UseCase Tests ---

    def test_create_note_success(self):
        """ノート作成成功を検証"""
        actor_id = uuid4()
        self.actor_repo.get_by_id.return_value = MagicMock(spec=Actor)
        
        note = self.note_usecase.create_note(actor_id, "Hello world")
        self.assertEqual(note.content, "Hello world")
        self.assertEqual(note.author_id, actor_id)
        self.note_repo.save.assert_called_once()

    def test_create_note_with_attachments(self):
        """添付ファイル付きノート作成成功を検証"""
        actor_id = uuid4()
        self.actor_repo.get_by_id.return_value = MagicMock(spec=Actor)
        attachments_data = [{"type": "Image", "url": "http://example.com/a.png", "mime_type": "image/png"}]
        
        note = self.note_usecase.create_note(actor_id, "With image", attachments_data)
        self.assertEqual(len(note.attachments), 1)
        self.assertEqual(note.attachments[0].type, "Image")

    def test_delete_note_success(self):
        """ノート削除成功を検証"""
        note_id = uuid4()
        actor_id = uuid4()
        mock_note = MagicMock(spec=Note)
        mock_note.author_id = actor_id
        self.note_repo.get_by_id.return_value = mock_note
        
        result = self.note_usecase.delete_note(note_id, actor_id)
        self.assertTrue(result)
        self.note_repo.delete.assert_called_once_with(note_id)

    def test_delete_note_unauthorized(self):
        """他人のノートを削除しようとした場合の失敗を検証"""
        note_id = uuid4()
        actor_id = uuid4()
        other_id = uuid4()
        mock_note = MagicMock(spec=Note)
        mock_note.author_id = other_id
        self.note_repo.get_by_id.return_value = mock_note
        
        with self.assertRaises(PermissionError):
            self.note_usecase.delete_note(note_id, actor_id)

if __name__ == "__main__":
    unittest.main()
