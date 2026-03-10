-- SQL Script to create tables for SNS Application
-- Compatible with SQLite, MariaDB, and PostgreSQL where possible

-- Actors Table
CREATE TABLE IF NOT EXISTS actors (
    id CHAR(36) PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    preferred_username VARCHAR(255),
    public_key TEXT NOT NULL,
    private_key TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Notes Table
CREATE TABLE IF NOT EXISTS notes (
    id CHAR(36) PRIMARY KEY,
    author_id CHAR(36) NOT NULL,
    content TEXT,
    published_at DATETIME NOT NULL,
    FOREIGN KEY (author_id) REFERENCES actors(id) ON DELETE CASCADE
);

-- Attachments Table
CREATE TABLE IF NOT EXISTS attachments (
    id CHAR(36) PRIMARY KEY,
    note_id CHAR(36) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'Image' or 'Video'
    url TEXT NOT NULL,
    mime_type VARCHAR(100),
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
);

-- Relationships Table (Following/Followers)
CREATE TABLE IF NOT EXISTS relationships (
    id CHAR(36) PRIMARY KEY,
    follower_id CHAR(36) NOT NULL,
    following_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(follower_id, following_id),
    FOREIGN KEY (follower_id) REFERENCES actors(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES actors(id) ON DELETE CASCADE
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_notes_author ON notes(author_id);
CREATE INDEX IF NOT EXISTS idx_attachments_note ON attachments(note_id);
CREATE INDEX IF NOT EXISTS idx_relationships_follower ON relationships(follower_id);
CREATE INDEX IF NOT EXISTS idx_relationships_following ON relationships(following_id);
