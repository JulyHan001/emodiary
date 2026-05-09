## ADDED Requirements

### Requirement: Emotion classification from natural language
The system SHALL accept user natural language text input and return a structured emotion analysis result containing: emotion category (one of: happy, sad, anxious, angry, calm, excited, confused), emotion intensity score (float 0.0-1.0), extracted keywords (2-5 items), and a one-sentence summary.

#### Scenario: Standard emotion detection
- **WHEN** user inputs "今天工作压力好大，deadline快到了，晚上都睡不好"
- **THEN** the system returns a JSON object with emotion "anxious", score between 0.5-0.9, keywords containing work-related terms, and a summary mentioning work pressure

#### Scenario: Positive emotion detection
- **WHEN** user inputs "今天升职加薪了！太开心了！"
- **THEN** the system returns emotion "happy" or "excited" with score >= 0.7

#### Scenario: Ambiguous or short input
- **WHEN** user inputs very short text like "还行吧"
- **THEN** the system SHALL still return a valid emotion analysis with emotion "calm" and a lower intensity score

### Requirement: Emotion analysis output validation
The system SHALL validate the LLM output and ensure all fields conform to the expected schema. If the LLM returns malformed JSON or out-of-range values, the system SHALL apply fallback handling.

#### Scenario: Malformed LLM output
- **WHEN** the LLM returns invalid JSON or missing fields
- **THEN** the system SHALL attempt to parse what is available and fill in defaults (emotion="calm", score=0.5, keywords=[], summary from original input)

#### Scenario: Score out of range
- **WHEN** the LLM returns a score > 1.0 or < 0.0
- **THEN** the system SHALL clamp the score to the [0.0, 1.0] range
