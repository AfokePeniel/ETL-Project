-- ==================== TRANSACTIONS TABLE ====================
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id   VARCHAR(20)   PRIMARY KEY,                                                -- unique ID, no duplicates
    account_number   VARCHAR(20)   NOT NULL,                                                   -- account the transaction belongs to
    account_type     VARCHAR(20)   NOT NULL CHECK (account_type IN ('chequing', 'savings', 'credit')),  -- only valid types
    transaction_type VARCHAR(20)   NOT NULL,                                                   -- deposit, withdrawal, transfer, payment
    amount           NUMERIC(12,2) NOT NULL,                                                   -- exact money value, never blank
    transaction_date DATE          NOT NULL,                                                   -- real date type
    processed_at     TIMESTAMP     NOT NULL                                                    -- when the transform ran (UTC)
);
