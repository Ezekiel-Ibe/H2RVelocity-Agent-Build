-- ==============================================================================
-- Microsoft Fabric Warehouse DDL & Stored Procedures
-- Server: emmyyfoj4mkuvbfl3hzr2r5wqe-uk5syzrintyuvnan5ivreqn7ku.datawarehouse.fabric.microsoft.com
-- Database: edm_wh_dev
-- Solution: Hire to Retire (H2R) Payroll Assurance Capability Agents (A01 - A09)
-- ==============================================================================

CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS governance;

-- ------------------------------------------------------------------------------
-- 1. SILVER LAYER ENTITIES (Canonical Workforce & Payroll Master)
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS silver.dim_worker (
    worker_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    worker_type VARCHAR(20) NOT NULL, -- 'employee', 'contingent', 'agent'
    status VARCHAR(20) NOT NULL,      -- 'active', 'onboarding', 'leaver'
    hire_date DATE NOT NULL,
    term_date DATE NULL,
    pay_group VARCHAR(20) NOT NULL,   -- 'MONTHLY', 'WEEKLY'
    fte DECIMAL(4,2) NOT NULL DEFAULT 1.0,
    job_id VARCHAR(50) NULL,
    org_id VARCHAR(50) NULL,
    has_approved_comp_change BIT NOT NULL DEFAULT 0,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE IF NOT EXISTS silver.fact_pay_item (
    pay_item_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    payroll_run_id VARCHAR(50) NOT NULL,
    period_id VARCHAR(20) NOT NULL, -- e.g. '2026-06'
    is_current_period BIT NOT NULL DEFAULT 1,
    worker_id VARCHAR(50) NOT NULL,
    base_pay DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    allowances DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    overtime DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    gross DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    tax DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    ni DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    pension DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    other_deductions DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    net DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    tax_code VARCHAR(20) NULL,
    ni_category VARCHAR(10) NULL,
    rti_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    approved_by VARCHAR(100) NULL,
    changed_fields VARCHAR(500) NULL, -- comma separated or JSON
    snapshot_hash VARCHAR(64) NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE IF NOT EXISTS silver.dim_time_record (
    time_record_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    worker_id VARCHAR(50) NOT NULL,
    period_id VARCHAR(20) NOT NULL,
    contracted_hours DECIMAL(6,2) NOT NULL,
    worked_hours DECIMAL(6,2) NOT NULL,
    absence_days DECIMAL(4,2) NOT NULL DEFAULT 0.0,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE IF NOT EXISTS silver.dim_lifecycle_event (
    event_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    event_type VARCHAR(30) NOT NULL, -- 'joiner', 'mover', 'leaver', 'payrun'
    worker_id VARCHAR(50) NOT NULL,
    event_date DATE NOT NULL,
    source_system VARCHAR(50) NOT NULL, -- 'HCM', 'Payroll', 'Identity'
    processed_flag BIT NOT NULL DEFAULT 0,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

-- ------------------------------------------------------------------------------
-- 2. GOLD LAYER ASSURANCE CASE MANAGEMENT & AUDIT
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gold.fact_assurance_case (
    case_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    payroll_run_id VARCHAR(50) NOT NULL,
    period_id VARCHAR(20) NOT NULL,
    case_state VARCHAR(30) NOT NULL,
    period_risk_score DECIMAL(5,2) NULL,
    total_anomalies INT NOT NULL DEFAULT 0,
    blocking_dq_errors INT NOT NULL DEFAULT 0,
    correlation_id VARCHAR(64) NOT NULL,
    idempotency_key VARCHAR(64) NOT NULL,
    sla_due_date DATETIME2 NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    closed_at DATETIME2 NULL
);

CREATE TABLE IF NOT EXISTS gold.fact_case_anomaly (
    anomaly_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    case_id VARCHAR(50) NOT NULL,
    worker_id VARCHAR(50) NOT NULL,
    anomaly_class VARCHAR(50) NOT NULL, -- leaver_still_paid, joiner_not_paid, unexplained_variance, missing_tax_code, negative_net_pay, duplicate_pay_record, unapproved_pay_change
    severity VARCHAR(20) NOT NULL,
    rule_version VARCHAR(20) NOT NULL,
    current_gross DECIMAL(18,2) NULL,
    prior_gross DECIMAL(18,2) NULL,
    variance_amount DECIMAL(18,2) NULL,
    variance_pct DECIMAL(7,4) NULL,
    explanation_narrative VARCHAR(MAX) NULL,
    root_cause_summary VARCHAR(500) NULL,
    system_of_record VARCHAR(50) NULL,
    resolution_state VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE IF NOT EXISTS gold.fact_case_correction (
    correction_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    case_id VARCHAR(50) NOT NULL,
    anomaly_id VARCHAR(50) NOT NULL,
    worker_id VARCHAR(50) NOT NULL,
    correction_option_type VARCHAR(50) NOT NULL,
    original_net DECIMAL(18,2) NOT NULL,
    expected_recalc_net DECIMAL(18,2) NOT NULL,
    actual_recalc_net DECIMAL(18,2) NULL,
    approval_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    approved_by VARCHAR(100) NULL,
    approval_timestamp DATETIME2 NULL,
    approval_rationale VARCHAR(1000) NULL,
    commit_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    commit_receipt_ref VARCHAR(100) NULL,
    validation_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

-- ------------------------------------------------------------------------------
-- 3. GOVERNANCE & AGENTOPS LOGGING (EU AI Act & ISO 42001 Conformance)
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS governance.agent_registry (
    agent_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    agent_name VARCHAR(100) NOT NULL,
    domain VARCHAR(20) NOT NULL DEFAULT 'HR',
    agent_class VARCHAR(30) NOT NULL, -- 'Experience', 'Orchestration', 'Task', 'Insight', 'Control'
    autonomy_level VARCHAR(20) NOT NULL DEFAULT 'L2_Augmented',
    model_deployment VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    total_executions INT NOT NULL DEFAULT 0,
    drift_detected BIT NOT NULL DEFAULT 0,
    sod_compliant BIT NOT NULL DEFAULT 1,
    last_certified_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE IF NOT EXISTS governance.audit_evidence_pack (
    pack_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    case_id VARCHAR(50) NOT NULL,
    payroll_run_id VARCHAR(50) NOT NULL,
    manifest_hash VARCHAR(64) NOT NULL,
    total_records_analyzed INT NOT NULL,
    total_anomalies_resolved INT NOT NULL,
    immutable_manifest_json VARCHAR(MAX) NOT NULL,
    attested_by_agent VARCHAR(50) NOT NULL,
    closure_attestation_state VARCHAR(20) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE IF NOT EXISTS governance.agentops_governance_log (
    log_id VARCHAR(50) NOT NULL PRIMARY KEY NONCLUSTERED,
    case_id VARCHAR(50) NOT NULL,
    correlation_id VARCHAR(64) NOT NULL,
    workflow_step VARCHAR(10) NOT NULL,
    agent_id VARCHAR(50) NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    actor_identity VARCHAR(100) NOT NULL,
    actor_role VARCHAR(50) NOT NULL,
    input_hash VARCHAR(64) NOT NULL,
    output_hash VARCHAR(64) NOT NULL,
    sod_check_result BIT NOT NULL DEFAULT 1,
    details_json VARCHAR(MAX) NULL,
    logged_at DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);
