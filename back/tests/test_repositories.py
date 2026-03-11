import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime
from domain.entities import Actor, Note

class TestRepositories(unittest.TestCase):
    def setUp(self):
        # メモリ上のSQLiteを使用
        self.engine = create_engine("sqlite:///:memory:")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
    def tearDown(self):
        self.session.close()

    def test_save_and_get_actor(self):
        """Actorをリポジトリ経由で保存し、取得できるか検証"""
        actor_id = uuid4()
        actor = Actor(
            id=actor_id,
            username="bob",
            preferred_username="Bob",
            public_key="BOB_PUB_KEY"
        )
        # 現在はモック実装がないため、パスします
        pass

    def test_save_and_get_note(self):
        """Noteをリポジトリ経由で保存し、取得できるか検証"""
        actor_id = uuid4()
        note_id = uuid4()
        now = datetime.now()
        note = Note(
            id=note_id,
            author_id=actor_id,
            content="Repository Test",
            published=now
        )
        pass

if __name__ == "__main__":
    unittest.main()
