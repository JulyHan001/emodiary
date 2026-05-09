## ADDED Requirements

### Requirement: Generate weekly/monthly emotion trend report
The system SHALL generate a growth insight report by aggregating historical diary entries over a specified period (week or month), analyzing emotion trends, identifying key events and recurring patterns, and providing actionable suggestions.

#### Scenario: Weekly report generation
- **WHEN** user requests a weekly report and has at least 3 diary entries in the past 7 days
- **THEN** the system generates a markdown report containing: emotion trend summary, key events that affected mood, pattern identification, and 1-2 actionable suggestions

#### Scenario: Monthly report generation
- **WHEN** user requests a monthly report
- **THEN** the system aggregates all diary entries for the specified month and generates a comprehensive report

#### Scenario: Insufficient data
- **WHEN** user requests a report but has fewer than 2 diary entries in the period
- **THEN** the system returns a friendly message explaining that more diary entries are needed to generate meaningful insights

### Requirement: Report uses real diary data via RAG
The report generation SHALL retrieve relevant diary entries from both SQLite (structured data for statistics) and ChromaDB (semantic context) to ground the report in actual user data, avoiding hallucination.

#### Scenario: Data-grounded report
- **WHEN** a report is generated
- **THEN** every trend and event mentioned in the report corresponds to actual diary entries retrievable from storage

### Requirement: Report output format
The report SHALL be formatted in Markdown with sections: 情绪趋势 (Emotion Trend), 关键事件 (Key Events), 模式识别 (Pattern Recognition), 成长建议 (Growth Suggestions).

#### Scenario: Report structure
- **WHEN** a report is generated
- **THEN** the output contains all four section headers in markdown format
