import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime
from back.domain.entities import Actor, Note
# これから作成するリポジトリとテーブル定義をインポート（想定）
# from back.infrastructure.database import Base, ActorTable, NoteTable
# from back.infrastructure.repositories import SQLActorRepository, SQLNoteRepository

class TestRepositories(unittest.TestCase):
    def setUp(self):
        # メモリ上のSQLiteを使用
        self.engine = create_engine("sqlite:///:memory:")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
        # 本来はBase.metadata.create_all(self.engine)などでテーブル作成を行う
        # self.actor_repo = SQLActorRepository(self.session)
        # self.note_repo = SQLNoteRepository(self.session)

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
        
        # self.actor_repo.save(actor)
        # retrieved_actor = self.actor_repo.get_by_id(actor_id)
        
        # self.assertIsNotNone(retrieved_actor)
        # self.assertEqual(retrieved_actor.username, "bob")
        # self.assertEqual(retrieved_actor.id, actor_id)
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
        
        # self.note_repo.save(note)
        # retrieved_note = self.note_repo.get_by_id(note_id)
        
        # self.assertIsNotNone(retrieved_note)
        # self.assertEqual(retrieved_note.content, "Repository Test")
        # self.assertEqual(retrieved_note.id, note_id)
        pass

    def test_get_notes_by_author(self):
        """特定のActorが作成したNote一覧を取得できるか検証"""
        actor_id = uuid4()
        # 複数のNoteを作成
        # notes = [
        #     Note(id=uuid4(), author_id=actor_id, content=f"Note {i}", published=datetime.now())
        #     for i in range(3)
        # ]
        # for n in notes:
        #     self.note_repo.save(n)
            
        # retrieved_notes = self.note_repo.get_by_author(actor_id)
        # self.assertEqual(len(retrieved_notes), 3)
        pass

if __name__ == "__main__":
    unittest.main()
