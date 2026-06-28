-- GuardShield AI - Enterprise Database Schema Configuration
-- Targets: PostgreSQL 15+

-- Enforce strict relational consistency mechanisms
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Create specialized extensions if not already present
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Define Application Operational Enumerations
CREATE TYPE user_role_enum AS ENUM ('COMPLIANCE_OFFICER', 'RISK_ANALYST', 'SYSTEM_ADMIN');
CREATE TYPE audit_status_enum AS ENUM ('PASSED', 'WARNING', 'FAILED_GUARDRAIL', 'MANUAL_REVIEW');

-- System Users Table
CREATE TABLE IF NOT EXISTS system_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role user_role_enum NOT NULL DEFAULT 'RISK_ANALYST',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Transaction Audit Logs (Core Ledger)
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES system_users(id) ON DELETE SET NULL,
    transaction_reference VARCHAR(100) UNIQUE NOT NULL,
    raw_payload TEXT NOT NULL,
    cleaned_payload TEXT,
    compliance_status audit_status_enum NOT NULL DEFAULT 'MANUAL_REVIEW',
    latency_ms INT NOT NULL,
    token_cost NUMERIC(10, 5) DEFAULT 0.00000,
    eval_score NUMERIC(5, 2),
    meta_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Performance Optimization Indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON system_users(email);
CREATE INDEX IF NOT EXISTS idx_audit_status ON audit_logs(compliance_status);
CREATE INDEX IF NOT EXISTS idx_audit_jsonb_meta ON audit_logs USING gin (meta_data);
CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_logs(created_at DESC);

-- Automated Timestamp Update Trigger Function
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_system_users_modtime
    BEFORE UPDATE ON system_users
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();