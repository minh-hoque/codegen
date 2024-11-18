from datetime import datetime
from typing import Dict, List, Optional
import uuid
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import os
from dotenv import load_dotenv


class MongoDB:
    def __init__(
        self,
        connection_string: Optional[str] = None,
        db_name: str = "coding_challenges",
    ):
        """
        Initialize MongoDB connection
        Args:
            connection_string: MongoDB Atlas connection string
            db_name: Name of the database
        """
        # Load environment variables
        load_dotenv()

        # Use provided connection string or get from environment
        self.connection_string = connection_string or os.getenv("MONGODB_URI")
        if not self.connection_string:
            raise ValueError(
                "MongoDB connection string not provided and MONGODB_URI not found in environment"
            )

        try:
            self.client = MongoClient(self.connection_string)
            # Test the connection
            self.client.admin.command("ping")
            print("Successfully connected to MongoDB Atlas")

            self.db: Database = self.client[db_name]
            self.questions: Collection = self.db.questions

            # Create an index on the id field if it doesn't exist
            self.questions.create_index("id", unique=True)

        except Exception as e:
            print(f"Error connecting to MongoDB Atlas: {e}")
            raise

    def save_question(self, question_data: Dict) -> str:
        """Save or update a question in the database"""
        # Generate unique ID if not exists
        question_id = question_data.get("id", str(uuid.uuid4()))
        question_data["id"] = question_id
        question_data["last_updated"] = datetime.now()

        # Update existing or insert new
        self.questions.update_one(
            {"id": question_id}, {"$set": question_data}, upsert=True
        )

        return question_id

    def get_question(self, question_id: str) -> Optional[Dict]:
        """Get a specific question by ID"""
        question = self.questions.find_one({"id": question_id})
        if question:
            # Remove MongoDB's _id field
            question.pop("_id", None)
            return question
        return None

    def get_all_questions(self) -> List[Dict]:
        """Get all questions"""
        questions = list(self.questions.find({}))
        # Remove MongoDB's _id field from each document
        for question in questions:
            question.pop("_id", None)
        return questions

    def update_question_status(self, question_id: str, status: str):
        """Update the status of a question"""
        self.questions.update_one(
            {"id": question_id},
            {"$set": {"status": status, "last_updated": datetime.now()}},
        )

    def close(self):
        """Close the MongoDB connection"""
        self.client.close()
