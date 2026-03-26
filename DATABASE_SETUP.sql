-- ============================================
-- SmartBiz Database Setup for Supabase
-- ============================================
-- Copy and paste this entire SQL into your Supabase SQL Editor
-- and execute it to create all tables
-- ============================================

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tasks table
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

-- Create reports table
CREATE TABLE IF NOT EXISTS reports (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    report_type TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path TEXT
);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id BIGSERIAL PRIMARY KEY,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT,
    sent_at TIMESTAMP,
    status TEXT CHECK (status IN ('pending', 'sent', 'failed')) DEFAULT 'pending'
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_employees_email ON employees(email);

-- Insert sample data (optional)
INSERT INTO employees (name, email, department)
VALUES ('Admin User', 'admin@example.com', 'Management')
ON CONFLICT (email) DO NOTHING;

-- Verify tables were created
SELECT 'employees' as table_name, COUNT(*) as record_count FROM employees
UNION ALL
SELECT 'tasks' as table_name, COUNT(*) as record_count FROM tasks
UNION ALL
SELECT 'reports' as table_name, COUNT(*) as record_count FROM reports
UNION ALL
SELECT 'notifications' as table_name, COUNT(*) as record_count FROM notifications;
