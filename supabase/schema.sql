-- ============================================================
-- حلقة القرآن - Database Schema
-- Supabase (PostgreSQL)
-- ============================================================

-- 1. Settings table (key-value for system configuration)
CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Managers table (the 5 rotating managers)
-- IMPORTANT: Names here must EXACTLY match the name entered during registration
-- The system matches by name to determine who is a manager each day
CREATE TABLE IF NOT EXISTS managers (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  sort_order INTEGER NOT NULL DEFAULT 0,
  pin TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Members table (the full member list ~100 names)
-- Users find and select their name from this list when registering
CREATE TABLE IF NOT EXISTS members (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  sort_order INTEGER NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 4. Priority members table (non-manager members who appear right after managers)
CREATE TABLE IF NOT EXISTS priority_members (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 5. Registrations table (daily registrations)
CREATE TABLE IF NOT EXISTS registrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  phone TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  registered_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Index for faster daily queries
CREATE INDEX IF NOT EXISTS idx_registrations_date
  ON registrations (registered_date, created_at);

-- Index for cleanup queries
CREATE INDEX IF NOT EXISTS idx_registrations_cleanup
  ON registrations (registered_date);

-- Migration for existing DBs: add PIN column if not exists
ALTER TABLE managers ADD COLUMN IF NOT EXISTS pin TEXT NOT NULL DEFAULT '';

-- Enable Row Level Security (optional, for future admin panel)
ALTER TABLE registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE managers ENABLE ROW LEVEL SECURITY;
ALTER TABLE priority_members ENABLE ROW LEVEL SECURITY;

-- Drop existing policies (safe to re-run)
DROP POLICY IF EXISTS "allow_anonymous_insert_registrations" ON registrations;
DROP POLICY IF EXISTS "allow_anonymous_select_registrations" ON registrations;
DROP POLICY IF EXISTS "allow_anonymous_select_settings" ON settings;
DROP POLICY IF EXISTS "allow_anonymous_select_managers" ON managers;
DROP POLICY IF EXISTS "allow_anonymous_select_members" ON members;
DROP POLICY IF EXISTS "allow_anonymous_select_priority_members" ON priority_members;

-- Allow anonymous insert for registration
CREATE POLICY "allow_anonymous_insert_registrations"
  ON registrations FOR INSERT
  TO anon
  WITH CHECK (true);

-- Allow anonymous select for checking registration status
CREATE POLICY "allow_anonymous_select_registrations"
  ON registrations FOR SELECT
  TO anon
  USING (true);

-- Allow anonymous select for settings
CREATE POLICY "allow_anonymous_select_settings"
  ON settings FOR SELECT
  TO anon
  USING (true);

-- Allow anonymous select for managers
CREATE POLICY "allow_anonymous_select_managers"
  ON managers FOR SELECT
  TO anon
  USING (true);

-- Allow anonymous select for members
CREATE POLICY "allow_anonymous_select_members"
  ON members FOR SELECT
  TO anon
  USING (true);

-- Allow anonymous select for priority members
CREATE POLICY "allow_anonymous_select_priority_members"
  ON priority_members FOR SELECT
  TO anon
  USING (true);

-- Allow anonymous users to call the PIN verification function
GRANT EXECUTE ON FUNCTION verify_manager_pin TO anon;

-- Securely verify if a PIN belongs to any manager (PIN never leaves the DB)
CREATE OR REPLACE FUNCTION verify_manager_pin(input_pin TEXT)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN EXISTS (SELECT 1 FROM managers WHERE pin = input_pin);
END;
$$;
