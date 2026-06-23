# Architecture Documentation - Financer AI

## System Overview

Financer AI is a hybrid system combining:
1. **Deterministic Logic**: For structured queries (dates, categories, totals)
2. **LLM-based RAG**: For flexible, open-ended questions
3. **Analytics Engine**: For forecasting, trends, and affordability analysis

## Core Components

### 1. Data Layer

#### `data_loader.py`
**Responsibility**: Ingest and normalize expense data

**Key Functions**:
- `load_data(file_path)`: Load CSV/Excel file
  - Normalize dates to datetime objects
  - Convert prices to float
  - Remove invalid entries (price=0)
  - Map categories
  - Create RAG documents

**Output**: 
- Pandas DataFrame with columns: `date`, `price`, `category`, `expense`
- List of formatted documents for embedding

**Design Pattern**: Single entry point for all data ingestion

---

#### `embedder.py`
**Responsibility**: Convert expense descriptions to vector embeddings

**Key Functions**:
- `generate_embeddings(docs, batch_size=32)`: Create embeddings for documents
  - Uses Sentence Transformers (all-MiniLM-L6-v2)
  - Batches for efficiency
  - Caches to disk for fast reloads

**Caching Strategy**:
```
Disk Cache (embeddings.npy + metadata.pkl)
    ↓ (if exists)
    Fast Load
    ↓ (if not)
    Generate → Cache
```

**Design Pattern**: Lazy loading with disk persistence

---

#### `rag_engine.py`
**Responsibility**: Vector search for expense data retrieval

**Key Functions**:
- `RAGDatabase.search(query_embedding, k=10)`: Find top-k similar expenses
  - Uses FAISS for efficient similarity search
  - Returns formatted expense strings

**Workflow**:
```
Query Text
    ↓
Embed Query
    ↓
FAISS Search (top-k neighbors)
    ↓
Format Results
    ↓
Return Context
```

**Design Pattern**: Vector database abstraction layer

---

### 2. Intent Detection Layer

#### `agents/intent_router.py`
**Responsibility**: Classify user query into intent categories

**Intent Classification**:
```python
Query Analysis:
├─ "buy/purchase/afford" + "bike/car/rs" → PURCHASE_ADVICE
├─ "advice/suggest/recommend" → FINANCIAL_ADVICE
├─ "total spend" (no month) → TOTAL_SPEND
├─ "forecast/future" → FORECAST
├─ "which/where/most/top" + "spend" → TOP_CATEGORY_SPEND
├─ "food" → CATEGORY_SPEND
├─ "save" → SAVINGS
├─ "overspending" → OVESPENDING
└─ DATE_KEYWORDS + month/year → MONTHLY_SPEND or DATE_SPEND
```

**Key Functions**:
- `detect_intent(query)`: Returns intent type as string

**Design Pattern**: Rule-based classifier with keyword matching

---

### 3. Finance Agent Layer

#### `agents/finance_agent.py`
**Responsibility**: Route queries and generate responses

**Handler Architecture**:
```
Query
    ↓
Intent Router
    ├─ PURCHASE_ADVICE → Purchase Handler
    │   └─ Extract price + date
    │   └─ Calculate affordability
    │   └─ Format recommendation
    │
    ├─ FORECAST → Forecast Handler
    │   └─ Get historical data
    │   └─ Fit trend line
    │   └─ Project 6 months
    │
    ├─ FINANCIAL_ADVICE → Advice Handler
    │   └─ Aggregate all metrics
    │   └─ Identify overspending
    │   └─ Generate suggestions
    │
    ├─ TOP_CATEGORY_SPEND → Category Handler
    │   └─ Group by category
    │   └─ Sort by amount
    │   └─ Return top-5
    │
    ├─ DATE/MONTHLY_SPEND → Time Handler
    │   └─ Filter by date
    │   └─ Sum amounts
    │   └─ Format result
    │
    └─ RAG → LLM Handler
        └─ Retrieve context
        └─ Build prompt
        └─ Call Groq API
        └─ Return response
```

**Response Generation**:
```python
# Deterministic (fast)
if intent in [TOTAL_SPEND, CATEGORY_SPEND, DATE_SPEND]:
    return calculate_from_data()

# Data-driven with trend analysis
elif intent in [FORECAST, TOP_CATEGORY_SPEND, PURCHASE_ADVICE]:
    return analyze_with_analytics()

# LLM-enriched
elif intent in [FINANCIAL_ADVICE, RAG]:
    return query_llm_with_context()
```

**Design Pattern**: Handler pattern with polymorphic routing

---

### 4. Analytics Layer

#### `tools/analytics_tools.py`
**Responsibility**: Compute financial metrics and predictions

**Key Functions**:

1. **`forecast_spending(df, periods=6)`**
   - Method: Linear regression on monthly totals
   - Input: Full expense DataFrame
   - Output: List of (month, predicted_amount) tuples
   - Accuracy: ±15-20% for trending data

2. **`spending_trend(df, months=6)`**
   - Analyzes last N months
   - Returns: "increasing/decreasing/stable" with rate of change
   - Use case: Identify spending patterns

3. **`calculate_purchase_affordability(df, target_price, months)`**
   - Calculates: 
     - Average monthly spend
     - Monthly savings needed
     - Monthly surplus/deficit
     - Months to afford
   - Returns: Dictionary with affordability metrics

4. **`detect_overspending(category_data, total_spend)`**
   - Alerts when category > 40% of total
   - Returns: List of alert strings

5. **`savings_suggestions(category_data)`**
   - Proposes 15% reduction per category
   - Returns: List of actionable suggestions

**Design Pattern**: Functional analytics library

---

### 5. LLM Service Layer

#### `ai_service.py`
**Responsibility**: Generate intelligent responses using Groq API

**Prompt Architecture**:
```
System Context:
├─ "You are a financial analyst"
├─ Period specification (if filtered)
├─ Data availability notice
│
Data Summary:
├─ Total records
├─ Date range
├─ Total spend
├─ Top 5 categories
├─ Recent 6 months trend
│
Detailed Context:
├─ 20-50 sample transactions
│   (row-based for date queries)
│   (semantic search for open queries)
│
User Query + Instructions:
├─ "Provide:"
├─ "1. Concise answer"
├─ "2. Spending patterns"
├─ "3. Practical suggestions"
```

**Key Functions**:
- `generate_answer_with_memory(query, db, filtered_df, ...)`
  - Builds context from filtered data
  - Retrieves similar transactions via RAG
  - Queries Groq LLM (llama-3.3-70b-versatile)
  - Returns formatted response

**LLM Configuration**:
- Model: llama-3.3-70b-versatile
- Provider: Groq (fast inference)
- Context length: ~4K tokens (sufficient for expense data)
- Temperature: Default (0.7)

**Design Pattern**: Template-based prompt generation

---

### 6. Date Extraction

#### `utils/date_extractor.py`
**Responsibility**: Parse natural language dates

**Supported Formats**:
- "June 2026", "Jun 2026" → (6, 2026, None)
- "23 June 2026", "23 Jun 2026" → (6, 2026, 23)
- "2026-06-23", "06/23/2026" → (6, 2026, 23)
- "last month", "this month" → Relative to today
- "yesterday", "today", "tomorrow" → Single dates

**Output**: Tuple (month, year, day) where day is optional

**Design Pattern**: Regex-based date parser with fallbacks

---

### 7. UI Components (Streamlit)

#### `pages/1_Overview.py`
- Dashboard with key metrics
- Monthly trend chart
- Top categories breakdown
- Recent transactions table

#### `pages/2_Category_Analysis.py`
- Category-specific drilldown
- Time-series trends per category
- Comparison with average

#### `pages/3_AI_Assistant.py`
- Chat interface
- Example queries display
- Conversation history

#### `components/chatbot.py`
**Key Functions**:
- `show_chatbot(db, all_data)`
  - Display chat input
  - Show example queries
  - Handle streaming responses

---

## Data Flow Diagrams

### Upload & Initialization Flow
```
User Uploads File
    ↓
app.py detects upload
    ↓
main.py@cache_data → load_data()
    ↓
data_loader.py
├─ Read CSV/Excel
├─ Normalize columns
├─ Validate data
└─ Create documents
    ↓
embedder.py@cache_data → generate_embeddings()
├─ Check disk cache
├─ Load or generate embeddings
└─ Cache to disk
    ↓
rag_engine.py → RAGDatabase
├─ Load embeddings
└─ Initialize FAISS index
    ↓
System Ready ✓
```

### Query Processing Flow
```
User Types Query
    ↓
intent_router.py
├─ Extract keywords
├─ Check for dates
└─ Classify intent
    ↓
finance_agent.py
├─ Route by intent
├─ Select handler
└─ Prepare data
    ↓
Handler Execution
├─ Deterministic: Analytics ⚡ (fast)
├─ LLM-based: AI Service 🧠 (flexible)
└─ RAG: Vector Search + LLM 🔍
    ↓
ai_service.py (if LLM path)
├─ Build context
├─ Query Groq API
└─ Format response
    ↓
chatbot.py
├─ Display response
├─ Update history
└─ Ready for next query
```

### Purchase Affordability Flow
```
User: "Can I buy ₹269000 bike in August?"
    ↓
intent_router: PURCHASE_ADVICE
    ↓
finance_agent.py
├─ Extract: price=269000, month=8, year=2026
├─ Calculate: months_until = days_to_august / 30
└─ Load: all historical spending data
    ↓
analytics_tools.py
├─ Calculate: avg_monthly_spend
├─ Calculate: monthly_needed = 269000 / months_until
├─ Calculate: monthly_surplus = avg_monthly - monthly_needed
├─ Determine: is_affordable = monthly_surplus >= 0
└─ Calculate: total_months_to_afford = 269000 / avg_monthly
    ↓
Response Generation
├─ If affordable: "✅ You CAN afford it by saving ₹X/month"
└─ If not: "❌ You need ₹X/month, have only ₹Y surplus"
    ↓
Action Plan
├─ "1. Track spending"
├─ "2. Cut expenses by ₹X"
└─ "3. Set savings goal"
```

---

## Performance Characteristics

### Time Complexity
| Operation | Complexity | Typical Time |
|-----------|-----------|--------------|
| Load data | O(n) | 100ms |
| Generate embeddings | O(n × d) | 2-5s (first time) |
| Search similar | O(log n) | 10ms |
| Category aggregation | O(n) | 50ms |
| Forecast | O(m) m=months | 5ms |
| LLM generation | O(context) | 2-5s |

### Space Complexity
| Component | Size |
|-----------|------|
| Embeddings (1000 rows) | ~400KB |
| DataFrame in memory | ~500KB per 1000 rows |
| FAISS index | ~300KB per 1000 embeddings |

---

## Error Handling

### Data Validation
```
Input Data
    ↓
Check columns exist
├─ If missing → Log error + skip
├─ If invalid type → Convert or skip
└─ If valid → Continue
    ↓
Filter invalid rows
├─ date=null → Skip
├─ price=0 → Skip
└─ category=null → Assign "Other"
    ↓
Cleaned Data
```

### Query Error Handling
```
User Query
    ↓
Try parsing
├─ If date parse fails → Use RAG
├─ If price extract fails → Request clarification
└─ If valid → Continue
    ↓
Try LLM call
├─ If API fails → Return error message
├─ If timeout → Return cached result if available
└─ If success → Return response
```

---

## Configuration & Customization

### Key Parameters

**Forecasting**:
```python
forecast_spending(df, periods=6)  # Months to forecast
```

**Purchase Affordability**:
```python
calculate_purchase_affordability(
    df, 
    target_price=269000,
    months_until_purchase=2  # Months to save
)
```

**Analytics**:
```python
spending_trend(df, months=6)  # Months to analyze
detect_overspending(categories, total, threshold=40)  # % threshold
```

**LLM**:
```python
model="llama-3.3-70b-versatile"  # Can swap model
temperature=0.7  # Creativity level
```

---

## Testing Strategy

### Unit Tests Needed
- Date extraction edge cases
- Category aggregation accuracy
- Affordability calculations
- Forecast accuracy

### Integration Tests Needed
- Full query pipeline
- Data upload + embedding generation
- RAG retrieval accuracy

### Example Test Cases
```python
# Affordability
def test_affordable_bike():
    df = sample_data_19250_monthly()
    result = calculate_purchase_affordability(df, 269000, 1)
    assert result['is_affordable'] == False
    assert result['total_available_months'] == 14

# Forecasting
def test_forecast():
    df = sample_monthly_increasing()
    forecast = forecast_spending(df, periods=6)
    assert len(forecast) == 6
    assert forecast[-1][1] > forecast[0][1]  # Increasing trend

# Intent Detection
def test_purchase_intent():
    query = "Can I buy a bike for 269000 in August?"
    assert detect_intent(query) == "PURCHASE_ADVICE"
```

---

## Security Considerations

1. **API Key**: Stored in `.env`, never logged
2. **Data Privacy**: Data stored locally, not sent to external services (except Groq LLM)
3. **SQL Injection**: Using pandas (safe), no raw SQL
4. **Input Validation**: All user inputs sanitized before processing

---

## Deployment Considerations

### Local Deployment
- Single-machine setup
- In-memory FAISS index
- Disk-based embedding cache

### Cloud Deployment
- Containerize with Docker
- Use cloud storage for data
- API key management via secrets
- Consider dedicated vector database (Pinecone, Weaviate)

### Scaling Strategy
```
Single Instance (current)
    ↓ (if needed)
Multiple Streamlit instances + shared FAISS
    ↓ (if further scaling)
Microservices: Analytics service + LLM service + API gateway
```

---

## Future Enhancement Roadmap

1. **Short-term** (1-2 weeks)
   - Add export functionality (PDF, Excel)
   - Budget goal tracking

2. **Medium-term** (1-2 months)
   - Multi-user support
   - Recurring expense detection
   - Advanced forecasting (ARIMA, Prophet)

3. **Long-term** (3-6 months)
   - Receipt OCR
   - Mobile app
   - Real-time expense import
   - Expense splitting

---

## References & Resources

- **Groq API**: https://console.groq.com/
- **Sentence Transformers**: https://www.sbert.net/
- **FAISS**: https://github.com/facebookresearch/faiss
- **Streamlit Docs**: https://docs.streamlit.io/
- **Pandas**: https://pandas.pydata.org/docs/
