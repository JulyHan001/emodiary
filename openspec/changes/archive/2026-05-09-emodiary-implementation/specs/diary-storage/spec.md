## ADDED Requirements

### Requirement: Create diary entry in SQLite
The system SHALL persist a diary entry to SQLite with fields: id (UUID), user_id, content (original user input), emotion, emotion_score, keywords (JSON array), summary, and created_at (UTC timestamp).

#### Scenario: Successful diary creation
- **WHEN** a valid DiaryEntry model is passed to the storage layer
- **THEN** a new row is inserted into the diary_entries table with all fields populated and a unique UUID

#### Scenario: Database table auto-creation
- **WHEN** the application starts and the diary_entries table does not exist
- **THEN** the system SHALL automatically create the table with the correct schema

### Requirement: Query diary entries by date range
The system SHALL support querying diary entries filtered by a date range (start_date, end_date).

#### Scenario: Date range query
- **WHEN** user requests diary entries from "2026-05-01" to "2026-05-07"
- **THEN** the system returns all diary entries with created_at within that range, ordered by created_at descending

#### Scenario: Empty result
- **WHEN** user queries a date range with no entries
- **THEN** the system returns an empty list

### Requirement: Query diary entries by emotion
The system SHALL support querying diary entries filtered by emotion category.

#### Scenario: Emotion filter query
- **WHEN** user requests diary entries with emotion "happy"
- **THEN** the system returns all diary entries where emotion equals "happy", ordered by created_at descending

### Requirement: Get all diary entries
The system SHALL support retrieving all diary entries for a user with optional pagination (limit, offset).

#### Scenario: Paginated listing
- **WHEN** user requests diary entries with limit=10 and offset=0
- **THEN** the system returns the 10 most recent diary entries

### Requirement: Async database operations
All SQLite operations SHALL be async using aiosqlite to avoid blocking the event loop.

#### Scenario: Concurrent request handling
- **WHEN** multiple API requests arrive simultaneously
- **THEN** database operations execute asynchronously without blocking other requests
