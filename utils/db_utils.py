import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import uuid


class JsonDB:
    def __init__(self, db_path: str = "data/questions.json"):
        self.db_path = Path(db_path)
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Create database file and parent directories if they don't exist"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self.db_path.write_text('{"questions": []}')

    def _read_db(self) -> Dict:
        """Read the database file"""
        return json.loads(self.db_path.read_text())

    def _write_db(self, data: Dict):
        """Write to the database file"""
        self.db_path.write_text(json.dumps(data, indent=2))

    def save_question(self, question_data: Dict) -> str:
        """Save or update a question in the database"""
        db_data = self._read_db()

        # Generate unique ID if not exists
        question_id = question_data.get("id", str(uuid.uuid4()))
        question_data["id"] = question_id
        question_data["last_updated"] = datetime.now().isoformat()

        # Update existing or add new
        questions = db_data["questions"]
        for i, q in enumerate(questions):
            if q.get("id") == question_id:
                questions[i] = question_data
                break
        else:
            question_data["created_at"] = datetime.now().isoformat()
            questions.append(question_data)

        self._write_db(db_data)
        return question_id

    def get_question(self, question_id: str) -> Optional[Dict]:
        """Get a specific question by ID"""
        db_data = self._read_db()
        for question in db_data["questions"]:
            if question.get("id") == question_id:
                return question
        return None

    def get_all_questions(self) -> List[Dict]:
        """Get all questions"""
        return self._read_db()["questions"]

    def update_question_status(self, question_id: str, status: str):
        """Update the status of a question"""
        db_data = self._read_db()
        for question in db_data["questions"]:
            if question.get("id") == question_id:
                question["status"] = status
                question["last_updated"] = datetime.now().isoformat()
                break
        self._write_db(db_data)
