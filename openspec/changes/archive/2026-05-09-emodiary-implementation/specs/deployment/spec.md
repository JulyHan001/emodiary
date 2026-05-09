## ADDED Requirements

### Requirement: Dockerfile for backend
The system SHALL provide a Dockerfile that builds the FastAPI backend application into a container image with all Python dependencies installed.

#### Scenario: Build backend image
- **WHEN** `docker build -t emodiary-backend .` is executed
- **THEN** a container image is created that can run the FastAPI server on port 8000

### Requirement: Docker Compose for full stack
The system SHALL provide a docker-compose.yml that starts both the FastAPI backend and Streamlit frontend, with shared volume for SQLite and ChromaDB data persistence.

#### Scenario: One-command startup
- **WHEN** `docker-compose up` is executed
- **THEN** both backend (port 8000) and frontend (port 8501) services start and are accessible

#### Scenario: Data persistence across restarts
- **WHEN** `docker-compose down` followed by `docker-compose up` is executed
- **THEN** previously stored diary entries and embeddings are still available

### Requirement: Environment variable configuration
The system SHALL support configuration via environment variables, with a .env.example file documenting all required variables (OPENAI_API_KEY) and optional variables (database path, ChromaDB path, ports).

#### Scenario: Configuration from environment
- **WHEN** the application starts with OPENAI_API_KEY set in environment
- **THEN** the application uses that key for all OpenAI API calls

#### Scenario: Missing required config
- **WHEN** the application starts without OPENAI_API_KEY
- **THEN** the application fails fast with a clear error message indicating the missing variable

### Requirement: Cloud deployment readiness
The system SHALL be deployable to Railway or Render with minimal configuration (environment variables only).

#### Scenario: Railway deployment
- **WHEN** the repository is connected to Railway with OPENAI_API_KEY set
- **THEN** the application builds and deploys successfully via the Dockerfile
