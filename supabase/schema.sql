-- Drop table if exists for clean init
DROP TABLE IF EXISTS rounds;

-- Create rounds table
CREATE TABLE rounds (
    id BIGSERIAL PRIMARY KEY,
    round_id TEXT UNIQUE NOT NULL,
    multiplier DECIMAL(10, 2) NOT NULL CHECK (multiplier >= 1.00),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    server_seed TEXT,
    client_seed TEXT,
    hash_value TEXT,
    players_count INTEGER DEFAULT 0,
    source TEXT DEFAULT 'collector'
);

-- Indexes for performance
CREATE UNIQUE INDEX idx_rounds_round_id ON rounds(round_id);
CREATE INDEX idx_rounds_timestamp ON rounds(timestamp DESC);

-- Enable Realtime publication
ALTER PUBLICATION supabase_realtime ADD TABLE rounds;
