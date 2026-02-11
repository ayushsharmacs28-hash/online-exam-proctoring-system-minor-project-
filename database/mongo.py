from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import sys

def init_db():
    """Initialize database connection with error handling"""
    try:
        client = MongoClient(
            "mongodb://localhost:27017/",
            serverSelectionTimeoutMS=5000
        )
        # Verify connection
        client.admin.command('ping')
        print("[OK] MongoDB connection successful")
        return client
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"[ERROR] MongoDB connection failed: {e}")
        print("\nPlease ensure MongoDB is running:")
        print("  - Windows: Run 'mongod' or start MongoDB service")
        print("  - Linux/Mac: Run 'sudo systemctl start mongod'")
        sys.exit(1)

# Initialize connection
client = init_db()
db = client["online_exam_proctor"]

# Collections
users = db["users"]
violations = db["violations"]
logs = db["exam_logs"]
exam_sessions = db["exam_sessions"]
exam_results = db["exam_results"]

# Create indexes for better performance
users.create_index("email", unique=True)
violations.create_index([("user_id", 1), ("time", -1)])
exam_sessions.create_index([("user_id", 1), ("start_time", -1)])
