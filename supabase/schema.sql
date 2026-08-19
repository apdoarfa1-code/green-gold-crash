-- Drop table if exists for clean init
DROP TABLE IF EXISTS rounds;

-- Create rounds table
CREATE TABLE rounds (
    id BIGSERIAL PRIMARY KEY,
    multiplier DECIMAL(10, 2) NOT NULL CHECK (multiplier >= 1.00),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    server_seed TEXT
);

-- Index for performance
CREATE INDEX idx_rounds_timestamp ON rounds(timestamp DESC);

-- Enable Realtime publication
ALTER PUBLICATION supabase_realtime ADD TABLE rounds;
