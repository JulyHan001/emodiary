## ADDED Requirements

### Requirement: Generate empathetic response based on emotion analysis
The system SHALL generate a warm, empathetic response based on the emotion analysis result and original user input. The response MUST first acknowledge the user's feelings, then provide one specific actionable suggestion.

#### Scenario: Response to negative emotion
- **WHEN** emotion analysis shows "sad" with score 0.8 and user mentioned work pressure
- **THEN** the response acknowledges the sadness, validates the feeling, and suggests a small actionable step (e.g., a break, a walk)

#### Scenario: Response to positive emotion
- **WHEN** emotion analysis shows "happy" with score 0.9
- **THEN** the response celebrates with the user and encourages them to note what made them happy

### Requirement: Response length and tone constraints
The empathy response SHALL be under 100 Chinese characters, use a warm and non-preachy tone, and avoid clinical language.

#### Scenario: Length compliance
- **WHEN** any empathy response is generated
- **THEN** the response is no longer than 100 Chinese characters

#### Scenario: Tone compliance
- **WHEN** any empathy response is generated
- **THEN** the response does not contain directive phrases like "你应该" or "你必须"
