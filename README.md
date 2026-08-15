# Financer AI - Personal Finance Assistant

An intelligent financial advisor that tracks your expenses, analyzes spending patterns, forecasts future spending, and provides data-driven purchase advice using AI.

## 🎯 Features

### Core Capabilities
- **Expense Tracking**: Upload and manage expense data from Excel/CSV files
- **Spending Analysis**: Categorize and analyze expenses by category and time period
- **AI Financial Advisor**: Get personalized financial advice using LLM (Groq API)
- **Purchase Planning**: Determine if you can afford major purchases and get a savings plan
- **Spending Forecasts**: Predict future spending patterns based on historical data
- **Smart Query Understanding**: Natural language questions about your finances

### Query Types Supported
- `"How much did I spend in June 2026?"` → Monthly spending totals
- `"Which categories do I spend the most on?"` → Top spending categories
- `"Can I buy a Royal Enfield Meteor bike (₹269,000) in August?"` → Purchase affordability analysis
- `"Give me financial advice"` → Comprehensive spending overview with recommendations
- `"Forecast my spending for next month"` → 6-month spending forecast
- `"What are my savings opportunities?"` → Actionable cost-reduction recommendations

## 📋 System Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design and component descriptions.

### High-Level Flow
```
User Query
    ↓
Intent Detection
    ├→ PURCHASE_ADVICE: Affordability calculator
    ├→ FORECAST: Spending predictor
    ├→ TOP_CATEGORY_SPEND: Category analyzer
    ├→ FINANCIAL_ADVICE: Comprehensive advisor
    ├→ DATE_SPEND/MONTHLY_SPEND: Historical queries
    └→ RAG: Semantic search on expense data
    ↓
Response Generation (deterministic or LLM-based)
    ↓
User Response
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip or conda
- Groq API key (for LLM features)

### Installation

1. **Clone/Setup the project**:
```bash
cd financer_ai
```

2. **Create virtual environment**:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

### Running the Application

```bash
streamlit run app.py
```

The app will launch at `http://localhost:8501`

## 📁 Project Structure

```
financer_ai/
├── README.md                      # This file
├── ARCHITECTURE.md               # System design documentation
├── requirements.txt              # Python dependencies
│
├── app.py                        # Streamlit app entry point
├── main.py                       # Core initialization & caching
│
├── data_loader.py               # Load & normalize expense data
├── embedder.py                  # Generate embeddings for RAG
├── rag_engine.py                # Vector search & retrieval
│
├── ai_service.py                # LLM prompt & response generation
├── categorizer.py               # Expense categorization
├── data_curation.py             # Data cleaning utilities
│
├── agents/                      # Intent-based query handlers
│   ├── intent_router.py        # Detect query type
│   └── finance_agent.py        # Route to handlers & generate responses
│
├── tools/                       # Domain-specific analytics
│   ├── analytics_tools.py      # Forecasting, trends, affordability
│   ├── budget_tools.py         # Budget tracking
│   ├── expense_tools.py        # Expense aggregation
│   └── forecasting_tools.py    # Prediction models
│
├── components/                  # Streamlit UI components
│   ├── overview.py             # Dashboard overview
│   ├── category_drilldown.py   # Category analysis
│   ├── charts.py               # Visualization
│   ├── insights.py             # Key insights
│   ├── filters.py              # Date/category filters
│   └── chatbot.py              # Chat interface
│
├── pages/                       # Streamlit pages
│   ├── 1_Overview.py           # Main dashboard
│   ├── 2_Category_Analysis.py  # Category drilldown
│   └── 3_AI_Assistant.py       # Chatbot page
│
└── utils/                       # Helper functions
    ├── helpers.py              # General utilities
    └── date_extractor.py       # Parse dates from text
```

## 🔄 Data Flow

### Expense Data Upload
```
Excel/CSV File
    ↓
data_loader.py (normalize dates, prices, categories)
    ↓
SQLite/In-Memory DataFrame
    ↓
embedder.py (generate embeddings for RAG)
    ↓
FAISS Vector DB
```

### Query Processing
```
Natural Language Query
    ↓
intent_router.py (detect intent)
    ↓
finance_agent.py (select handler)
    ├─→ Deterministic Handler (fast, date/category queries)
    └─→ LLM Handler (flexible, complex questions)
    ↓
ai_service.py (generate response with context)
    ↓
Streamlit Display
```

## 🎨 Key Components

### Intent Router (`agents/intent_router.py`)
Classifies queries into:
- `TOTAL_SPEND`: Total spending amount
- `DATE_SPEND`: Spending on specific date
- `MONTHLY_SPEND`: Spending in specific month
- `CATEGORY_SPEND`: Spending in category
- `TOP_CATEGORY_SPEND`: Top spending categories
- `FORECAST`: Future spending prediction
- `PURCHASE_ADVICE`: Can I afford this item?
- `FINANCIAL_ADVICE`: General financial guidance
- `SAVINGS`: Savings recommendations
- `OVESPENDING`: Overspending alerts
- `RAG`: Semantic search fallback

### Finance Agent (`agents/finance_agent.py`)
Routes queries to appropriate handlers:
- Deterministic handlers for structured queries (fast, accurate)
- LLM-based handler for open-ended questions (flexible, contextual)

### Analytics Tools (`tools/analytics_tools.py`)
- `calculate_purchase_affordability()`: Analyze if purchase is feasible
- `forecast_spending()`: Predict next 6 months
- `spending_trend()`: Detect spending direction
- `get_monthly_spend_series()`: Monthly aggregations

### AI Service (`ai_service.py`)
- Builds context-aware prompts with:
  - Spending summary (total, monthly average, trend)
  - Top categories
  - Recent monthly data
  - Date-specific filtering
- Uses Groq LLM for response generation
- Provides actionable financial insights

## 💾 Data Requirements

Expense data should have columns:
- `date`: Transaction date (any common format)
- `price`: Amount spent (numeric)
- `category`: Expense category (e.g., food, transport, utilities)
- `expense`: Item description

Example CSV:
```
date,price,category,expense
2026-01-15,150,food,lunch
2026-01-15,500,transport,uber
2026-01-16,1200,utilities,electricity
```

## 🔐 Environment Setup

Required environment variables:
```bash
GROQ_API_KEY=your_api_key
```

Optional customization:
```bash
STREAMLIT_LOGGER_LEVEL=error          # Reduce verbose logs
STREAMLIT_CLIENT_THEME=light/dark     # UI theme
```

## 📊 Performance Optimization

- **Embedding Cache**: Disk-based cache for embeddings (fast reload)
- **Streamlit Caching**: `@st.cache_data` for data operations
- **Vectorized Operations**: Pandas for fast aggregations
- **Lazy Loading**: Components load on-demand

## 🚨 Common Issues & Solutions

### Issue: "No spending data found for [month]"
**Solution**: Ensure data contains entries for that period. Use historical data for forecasting.

### Issue: Slow embedding generation
**Solution**: Embeddings are cached to disk. First run will be slow; subsequent runs will be fast.

### Issue: Groq API errors
**Solution**: Check your API key in `.env`. Verify account has credits.

## 📈 Future Enhancements

- [ ] Multi-user support with authentication
- [ ] Budget goal tracking
- [ ] Recurring expense detection
- [ ] Receipt OCR for automated expense entry
- [ ] Expense splitting & shared budgets
- [ ] Mobile app integration
- [ ] Export reports (PDF, Excel)
- [ ] Real-time notifications for overspending

## 🤝 Contributing

Contributions welcome! Please:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🆘 Support

For issues, questions, or suggestions:
1. Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
2. Review code comments in relevant modules
3. Test with sample data provided

## 👨‍💻 Author
Shrinath Jadhav - AI Data Engineer
Built with ❤️ for smarter personal finance management
