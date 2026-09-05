PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS artists (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS albums (id INTEGER PRIMARY KEY, artist_id INTEGER, title TEXT NOT NULL, year TEXT, artwork_key TEXT, UNIQUE(artist_id, title), FOREIGN KEY(artist_id) REFERENCES artists(id) ON DELETE SET NULL);
CREATE TABLE IF NOT EXISTS tracks (id TEXT PRIMARY KEY, path TEXT NOT NULL, filename TEXT NOT NULL, size_bytes INTEGER NOT NULL, modified_ns INTEGER NOT NULL, sha256 TEXT NOT NULL, title TEXT, artist TEXT, album TEXT, album_artist TEXT, genre TEXT, year TEXT, track_number TEXT, disc_number TEXT, duration_seconds REAL, has_artwork INTEGER NOT NULL DEFAULT 0, metadata_error TEXT, is_favorite INTEGER NOT NULL DEFAULT 0, rating INTEGER, play_count INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, CHECK (rating IS NULL OR (rating >= 1 AND rating <= 5)));
CREATE INDEX IF NOT EXISTS idx_tracks_artist ON tracks(artist);
CREATE INDEX IF NOT EXISTS idx_tracks_album ON tracks(album);
CREATE INDEX IF NOT EXISTS idx_tracks_title ON tracks(title);
CREATE INDEX IF NOT EXISTS idx_tracks_sha256 ON tracks(sha256);
CREATE INDEX IF NOT EXISTS idx_tracks_favorite ON tracks(is_favorite);
CREATE TABLE IF NOT EXISTS file_locations (id INTEGER PRIMARY KEY, track_id TEXT NOT NULL, path TEXT NOT NULL UNIQUE, filename TEXT NOT NULL, size_bytes INTEGER NOT NULL, modified_ns INTEGER NOT NULL, first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(track_id) REFERENCES tracks(id) ON DELETE CASCADE);
CREATE INDEX IF NOT EXISTS idx_file_locations_track ON file_locations(track_id);
CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS playlist_tracks (playlist_id INTEGER NOT NULL, track_id TEXT NOT NULL, position INTEGER NOT NULL DEFAULT 0, added_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (playlist_id, track_id), FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE, FOREIGN KEY(track_id) REFERENCES tracks(id) ON DELETE CASCADE);
CREATE INDEX IF NOT EXISTS idx_playlist_tracks_playlist_position ON playlist_tracks(playlist_id, position);
CREATE TABLE IF NOT EXISTS metadata_backups (id INTEGER PRIMARY KEY, track_id TEXT NOT NULL, source_path TEXT NOT NULL, backup_path TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(track_id) REFERENCES tracks(id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS play_history (id INTEGER PRIMARY KEY, track_id TEXT NOT NULL, played_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(track_id) REFERENCES tracks(id) ON DELETE CASCADE);
CREATE INDEX IF NOT EXISTS idx_play_history_track_time ON play_history(track_id, played_at);
