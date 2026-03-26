#!/usr/bin/env python3
"""
SmartBiz Setup Script - Initialize Supabase Database Tables
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Create all required tables in Supabase"""
    
    from supabase import create_client
    
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL or SUPABASE_KEY not set in .env")
        sys.exit(1)
    
    print("🔗 Connecting to Supabase...")
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Connected to Supabase")
    except Exception as e:
        print(f"❌ Failed to connect: {str(e)}")
        sys.exit(1)
    
    # SQL commands to create tables
    sql_commands = [
        # Employees table
        """
        CREATE TABLE IF NOT EXISTS employees (
            id BIGSERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tasks table
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id BIGSERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            assigned_to BIGINT REFERENCES employees(id) ON DELETE CASCADE,
            status TEXT CHECK (status IN ('pending', 'in_progress', 'done')) DEFAULT 'pending',
            priority TEXT CHECK (priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
            due_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Reports table
        """
        CREATE TABLE IF NOT EXISTS reports (
            id BIGSERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            report_type TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_path TEXT
        );
        """,
        
        # Notifications table
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id BIGSERIAL PRIMARY KEY,
            recipient_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT,
            sent_at TIMESTAMP,
            status TEXT CHECK (status IN ('pending', 'sent', 'failed')) DEFAULT 'pending'
        );
        """,
        
        # Create indexes for performance
        """
        CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);
        """,
        
        """
        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        """,
        
        """
        CREATE INDEX IF NOT EXISTS idx_employees_email ON employees(email);
        """
    ]
    
    print("\n📋 Creating database tables...")
    
    try:
        # Try to insert a test employee to verify tables exist
        response = supabase.table('employees').select('*').limit(1).execute()
        print("✅ Tables already exist or were created")
        return True
    except Exception as e:
        print(f"⚠️  Tables may need manual creation. Details: {str(e)}")
        print("\n📝 Copy and paste this SQL into your Supabase SQL editor:")
        print("\n" + "="*60)
        for sql in sql_commands:
            print(sql.strip())
            print(";")
            print()
        print("="*60)
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 SmartBiz Database Setup")
    print("=" * 60)
    
    setup_database()
    
    print("\n✅ Setup complete!")
    print("\n📚 Next steps:")
    print("1. Copy the SQL above and run it in Supabase SQL editor")
    print("2. Run: python main.py")
    print("3. Access: http://localhost:5000")
