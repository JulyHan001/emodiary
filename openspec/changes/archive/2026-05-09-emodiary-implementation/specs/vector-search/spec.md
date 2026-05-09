## ADDED Requirements

### Requirement: Store diary embeddings in ChromaDB
The system SHALL generate an embedding for each diary entry (using the concatenation of user content and AI summary) and store it in a ChromaDB collection with the diary UUID as document ID and metadata including emotion, emotion_score, and date.

#### Scenario: Embedding storage on diary creation
- **WHEN** a new diary entry is saved to SQLite
- **THEN** the system also generates an embedding via OpenAI text-embedding-3-small and stores it in the ChromaDB "diary_entries" collection

#### Scenario: Metadata attached to embedding
- **WHEN** an embedding is stored in ChromaDB
- **THEN** the metadata contains at minimum: emotion (string), emotion_score (float), date (ISO format string)

### Requirement: Semantic similarity search
The system SHALL support querying ChromaDB with a natural language question and returning the top-k most semantically similar diary entries.

#### Scenario: Retrieve similar entries
- **WHEN** user asks "我最近工作压力大吗"
- **THEN** the system generates an embedding for the query and returns the top 5 most similar diary entries from ChromaDB

#### Scenario: Filter by metadata
- **WHEN** a search is performed with a date range filter
- **THEN** the system applies ChromaDB metadata filtering to restrict results to entries within the specified date range

### Requirement: ChromaDB persistence
The ChromaDB collection SHALL persist to a local directory so data survives application restarts.

#### Scenario: Data persistence across restarts
- **WHEN** the application is stopped and restarted
- **THEN** all previously stored embeddings are still available for search

### Requirement: Collection initialization
The system SHALL create the ChromaDB collection on first use if it does not exist.

#### Scenario: First run initialization
- **WHEN** the application starts for the first time with no existing ChromaDB data
- **THEN** the system creates the "diary_entries" collection without error
