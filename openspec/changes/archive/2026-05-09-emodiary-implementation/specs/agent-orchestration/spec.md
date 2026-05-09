## ADDED Requirements

### Requirement: Diary recording workflow via LangGraph
The system SHALL implement a LangGraph StateGraph for the diary recording flow with nodes: emotion_detect → structured_extract → store → respond. Each node is an async function that reads from and writes to a shared TypedDict state.

#### Scenario: End-to-end diary recording
- **WHEN** user submits "今天被老板骂了，心情很差"
- **THEN** the workflow executes all four nodes in sequence and returns a state containing emotion_analysis, diary_entry (persisted), and empathy_response

#### Scenario: State propagation between nodes
- **WHEN** the emotion_detect node completes
- **THEN** the next node (structured_extract) can access the emotion analysis result from the shared state

### Requirement: History query workflow via LangGraph
The system SHALL implement a LangGraph StateGraph for history queries with an intent classification node that routes to either rag_search → synthesize, or report_gen, based on user intent.

#### Scenario: Query intent routing to RAG
- **WHEN** user asks "我上周心情怎么样"
- **THEN** the intent classifier routes to rag_search node, which retrieves relevant entries, then synthesize node generates an answer

#### Scenario: Query intent routing to report
- **WHEN** user asks "帮我生成这个月的情绪报告"
- **THEN** the intent classifier routes to report_gen node

#### Scenario: Casual chat fallback
- **WHEN** user inputs something that is neither diary recording nor history query (e.g., "你好")
- **THEN** the system responds with a friendly greeting without invoking the diary or query workflows

### Requirement: LangGraph state definition
The system SHALL define a TypedDict state containing: user_input (str), intent (str), emotion_analysis (EmotionAnalysis | None), diary_entry (DiaryEntry | None), response (str), retrieved_entries (list), report (str | None).

#### Scenario: Clean state initialization
- **WHEN** a new user message arrives
- **THEN** a fresh state is created with user_input populated and all other fields set to None or empty defaults

### Requirement: Intent classification
The system SHALL classify user input into one of three intents: "record_diary" (user expressing feelings), "query_history" (user asking about past entries), or "casual_chat" (general conversation).

#### Scenario: Diary recording intent
- **WHEN** user says "今天好累，加班到很晚"
- **THEN** intent is classified as "record_diary"

#### Scenario: History query intent
- **WHEN** user says "我这周都记录了什么"
- **THEN** intent is classified as "query_history"
