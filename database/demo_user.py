"""
Demo User Setup Script
Run this once to create demo student and admin accounts
"""

import bcrypt
from database.mongo import users

def create_demo_users():
    """Create demo student and admin users"""
    
    # Check if users already exist
    if users.find_one({"email": "student@demo.com"}):
        print("Demo users already exist!")
        return
    
    # Create student account
    student_password = bcrypt.hashpw("password123".encode(), bcrypt.gensalt())
    users.insert_one({
        "email": "student@demo.com",
        "password": student_password,
        "name": "Demo Student",
        "role": "student"
    })
    print("✓ Created student account: student@demo.com / password123")
    
    # Create admin account
    admin_password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
    users.insert_one({
        "email": "admin@demo.com",
        "password": admin_password,
        "name": "Admin User",
        "role": "admin"
    })
    print("✓ Created admin account: admin@demo.com / admin123")
    
    print("\n✓ Demo users created successfully!")

if __name__ == "__main__":
    create_demo_users()
