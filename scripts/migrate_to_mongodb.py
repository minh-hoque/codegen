import json
from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from utils.mongo_utils import MongoDB


def check_environment():
    """Check if MongoDB Atlas connection string is properly configured"""
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise EnvironmentError(
            "MONGODB_URI not found in environment variables.\n"
            "Please ensure you have a .env file with your MongoDB Atlas connection string:\n"
            "MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
        )
    if not mongodb_uri.startswith("mongodb+srv://"):
        raise EnvironmentError(
            "Invalid MongoDB URI. Please use a MongoDB Atlas connection string that starts with 'mongodb+srv://'"
        )


def migrate_json_to_mongodb():
    """Migrate data from local JSON file to MongoDB Atlas"""
    # Load environment variables
    load_dotenv()

    try:
        # Verify MongoDB Atlas configuration
        check_environment()

        # Read existing JSON data
        json_path = Path("data/questions.json")
        if not json_path.exists():
            print("No JSON data found to migrate")
            return

        # Initialize MongoDB Atlas connection
        print("Connecting to MongoDB Atlas...")
        mongo_db = MongoDB()

        with open(json_path, "r") as f:
            json_data = json.load(f)

        # Migrate each question
        total_questions = len(json_data.get("questions", []))
        if total_questions == 0:
            print("No questions found in JSON file")
            return

        print(f"Starting migration of {total_questions} questions to MongoDB Atlas...")
        migrated = 0

        for question in json_data.get("questions", []):
            try:
                mongo_db.save_question(question)
                migrated += 1
                print(
                    f"Migrated question {question.get('id')} ({migrated}/{total_questions})"
                )
            except Exception as e:
                print(f"Error migrating question {question.get('id')}: {str(e)}")

        success_rate = (migrated / total_questions) * 100
        print(f"\nMigration completed:")
        print(f"- Successfully migrated: {migrated}/{total_questions} questions")
        print(f"- Success rate: {success_rate:.1f}%")

    except Exception as e:
        print(f"\nMigration failed: {str(e)}")
        print("\nPlease ensure:")
        print("1. Your .env file exists and contains MONGODB_URI")
        print("2. The MongoDB Atlas connection string is correct")
        print("3. Your network can connect to MongoDB Atlas")
        print("4. Your IP address is whitelisted in MongoDB Atlas")
    finally:
        if "mongo_db" in locals():
            mongo_db.close()
            print("\nDatabase connection closed")


if __name__ == "__main__":
    migrate_json_to_mongodb()
