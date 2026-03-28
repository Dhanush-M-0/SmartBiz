-- =============================================
-- SmartBiz Supabase Schema
-- Run this in your Supabase SQL Editor
-- =============================================

-- Employees Table
CREATE TABLE IF NOT EXISTS employees (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tasks Table
CREATE TABLE IF NOT EXISTS tasks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    assigned_to UUID REFERENCES employees(id) ON DELETE SET NULL,
    status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending', 'In Progress', 'Done')),
    priority TEXT DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High')),
    deadline DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Reports Log Table
CREATE TABLE IF NOT EXISTS reports_log (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    report_type TEXT NOT NULL,
    file_name TEXT NOT NULL,
    generated_at TIMESTAMPTZ DEFAULT NOW()
);
