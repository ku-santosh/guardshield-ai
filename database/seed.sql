-- Seed Core Enterprise User Directory
-- Initial Passwords correspond to pre-hashed strings for testing environment verification ('GuardShield2026!')
INSERT INTO system_users (id, email, hashed_password, full_name, role, is_active)
VALUES 
('a6b0c231-1bf3-4b68-b76b-95689104f1a2', 'compliance.officer@ubs-mock.com', '$2b$12$Z0Gv66YqM7M/PqDFe7f.uugWun60qfM4VepIorE8tq7rJmKxN1XOW', 'Sarah Jenkins', 'COMPLIANCE_OFFICER', true),
('b4d1c932-2cf4-5c79-c87c-06790215f2b3', 'risk.analyst@ubs-mock.com', '$2b$12$Z0Gv66YqM7M/PqDFe7f.uugWun60qfM4VepIorE8tq7rJmKxN1XOW', 'David Miller', 'RISK_ANALYST', true)
ON CONFLICT (email) DO NOTHING;

-- Seed Baseline Reference Audit Data
INSERT INTO audit_logs (transaction_reference, raw_payload, cleaned_payload, compliance_status, latency_ms, token_cost, eval_score, meta_data)
VALUES 
('TXN-8849201', '{"amount": 5000000, "source": "unverified_offshore", "notes": "Urgent transfer from internal account containing confidential strategy details"}', '{"amount": 5000000, "source": "unverified_offshore", "notes": "Urgent transfer from internal account"}', 'WARNING', 142, 0.00320, 0.72, '{"risk_vectors": ["large_amount", "insider_leak_risk"], "flagged_terms": ["confidential strategy"]}')
ON CONFLICT (transaction_reference) DO NOTHING;