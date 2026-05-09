## ADDED Requirements

### Requirement: Chat interface tab
The system SHALL provide a Streamlit chat interface where users can type messages, see AI responses with emotion analysis results, and view conversation history within the session.

#### Scenario: Send message and receive response
- **WHEN** user types a message in the chat input and presses send
- **THEN** the system displays the user message, shows a loading indicator, then displays the AI response with emotion tag and empathy reply

#### Scenario: Display emotion tag
- **WHEN** an AI response is received from the chat API
- **THEN** the emotion category and score are displayed as a colored badge/tag above the response text

### Requirement: Emotion dashboard tab
The system SHALL provide an emotion dashboard showing: a pie chart of emotion distribution, a line chart of emotion scores over time, and summary statistics (total entries, most frequent emotion, average score).

#### Scenario: Dashboard with data
- **WHEN** user navigates to the emotion dashboard tab and has diary entries
- **THEN** the system displays pie chart, line chart, and summary stats based on actual diary data

#### Scenario: Dashboard without data
- **WHEN** user navigates to the emotion dashboard tab with no diary entries
- **THEN** the system displays a friendly message encouraging the user to start journaling

### Requirement: Diary history tab
The system SHALL provide a tab listing past diary entries in reverse chronological order, each showing: date, emotion tag, summary, and expandable full content.

#### Scenario: View diary list
- **WHEN** user navigates to the diary history tab
- **THEN** the system displays a scrollable list of diary entries with date, emotion, and summary visible

### Requirement: Growth report tab
The system SHALL provide a tab where users can request and view weekly/monthly growth insight reports rendered in markdown.

#### Scenario: Generate and view report
- **WHEN** user clicks "Generate Weekly Report" button
- **THEN** the system calls the /report API and renders the markdown report in the tab

### Requirement: Frontend communicates via HTTP API
The Streamlit frontend SHALL communicate exclusively with the FastAPI backend via HTTP requests (using the requests library or httpx). No direct imports of backend logic.

#### Scenario: API communication
- **WHEN** any frontend action requires data
- **THEN** the frontend makes an HTTP request to the appropriate FastAPI endpoint
