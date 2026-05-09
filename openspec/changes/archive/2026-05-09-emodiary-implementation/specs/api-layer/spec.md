## ADDED Requirements

### Requirement: POST /chat endpoint
The system SHALL provide a POST /chat endpoint that accepts a JSON body with user_input (string) and optional user_id (string, default "default"), invokes the LangGraph agent workflow, and returns the response including emotion analysis and empathy reply.

#### Scenario: Diary recording via chat
- **WHEN** a POST request is sent to /chat with body {"user_input": "今天好累"}
- **THEN** the system returns a JSON response containing: emotion_analysis (object), diary_entry (object with id), and response (string with empathy reply)

#### Scenario: History query via chat
- **WHEN** a POST request is sent to /chat with body {"user_input": "我这周心情怎么样"}
- **THEN** the system returns a JSON response with the synthesized answer based on retrieved diary entries

### Requirement: GET /diary endpoint
The system SHALL provide a GET /diary endpoint that returns diary entries with optional query parameters: start_date, end_date, emotion, limit (default 20), offset (default 0).

#### Scenario: List all diary entries
- **WHEN** a GET request is sent to /diary without filters
- **THEN** the system returns the 20 most recent diary entries

#### Scenario: Filter by date and emotion
- **WHEN** a GET request is sent to /diary?start_date=2026-05-01&end_date=2026-05-07&emotion=happy
- **THEN** the system returns only happy diary entries from that date range

### Requirement: GET /report endpoint
The system SHALL provide a GET /report endpoint that accepts query parameters: period (week or month), date (reference date, defaults to today), and returns a generated growth insight report.

#### Scenario: Generate weekly report
- **WHEN** a GET request is sent to /report?period=week
- **THEN** the system returns a JSON response with a markdown-formatted report for the past week

### Requirement: GET /search endpoint
The system SHALL provide a GET /search endpoint that accepts a query parameter q (search text) and top_k (default 5), performs semantic search via ChromaDB, and returns matching diary entries.

#### Scenario: Semantic search
- **WHEN** a GET request is sent to /search?q=工作压力&top_k=3
- **THEN** the system returns the top 3 semantically similar diary entries

### Requirement: Error handling and response format
All API endpoints SHALL return consistent JSON responses. Errors SHALL use appropriate HTTP status codes (400 for bad input, 500 for server errors) with a structured error response body containing "detail" field.

#### Scenario: Invalid request body
- **WHEN** a POST request is sent to /chat with missing user_input field
- **THEN** the system returns HTTP 422 with validation error details

#### Scenario: Server error
- **WHEN** an internal error occurs (e.g., LLM API failure)
- **THEN** the system returns HTTP 500 with a detail message
