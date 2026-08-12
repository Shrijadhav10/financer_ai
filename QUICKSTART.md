# Quick Start Guide - Financer AI

Get up and running in 5 minutes.

## ⚡ Quick Setup

### 1. Prerequisites Check
```bash
# Verify Python 3.9+
python --version

# Verify pip
pip --version
```

### 2. Install & Run
```bash
# Clone/navigate to project
cd financer_ai

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up your API key (required for AI features)
# Create .env file with:
# GROQ_API_KEY=your_key_here

# Launch app
streamlit run app.py
```

App opens at `http://localhost:8501` ✓

---

## 📊 Using the App

### Step 1: Upload Your Data
1. Go to **Overview** page
2. Click "Upload Expense Data"
3. Select your CSV/Excel file

**Expected Format**:
```
date,price,category,expense
2026-01-15,150,food,lunch
2026-01-15,500,transport,uber
2026-01-16,1200,utilities,electricity
2026-01-20,2500,food,groceries
```

### Step 2: View Dashboard
After upload, you'll see:
- Total spending
- Monthly trend chart
- Top 5 categories
- Recent transactions

### Step 3: Ask Questions
Go to **AI Assistant** and try these:

**Basic Questions**:
- `How much did I spend in January 2026?`
- `What are my top spending categories?`

**Purchase Planning**:
- `Can I buy a Royal Enfield Meteor bike (₹269000) in August?`
- `Can I afford a ₹500000 laptop?`

**Financial Advice**:
- `Give me financial advice`
- `How can I save more money?`

**Predictions**:
- `Forecast my spending for the next 6 months`
- `What's my spending trend?`

---

## 📁 Sample Data

Create a file `sample_expenses.csv`:
```
date,price,category,expense
2026-01-05,1200,food,groceries
2026-01-06,350,food,restaurant
2026-01-07,500,transport,fuel
2026-01-08,2000,utilities,internet
2026-01-10,800,entertainment,movies
2026-01-12,1500,food,groceries
2026-01-15,400,transport,uber
2026-01-18,3000,utilities,electricity
2026-02-02,1200,food,groceries
2026-02-05,450,food,lunch
2026-02-08,600,transport,fuel
2026-02-10,2000,utilities,water
2026-02-15,1800,food,groceries
2026-02-20,700,entertainment,games
2026-03-03,1300,food,groceries
2026-03-07,500,food,restaurant
2026-03-10,700,transport,fuel
2026-03-12,2500,utilities,electricity
2026-03-18,1900,food,groceries
2026-03-25,800,entertainment,concert
```

Upload this and try the queries!

---

## 🤖 AI Query Examples

### Example 1: Monthly Spending
**You ask**: `How much did I spend in January 2026?`

**AI responds**: 
```
Your spending in January 2026 is ₹5150
```

### Example 2: Top Categories
**You ask**: `Which categories do I spend the most on?`

**AI responds**:
```
Top spending categories for all time:
1. Food: ₹8500 (42.5%)
2. Utilities: ₹7500 (37.5%)
3. Transport: ₹2100 (10.5%)
4. Entertainment: ₹1800 (9.0%)
```

### Example 3: Purchase Affordability
**You ask**: `Can I buy a bike for 269000 rupees in August 2026?`

**AI responds**:
```
Purchase Analysis: Item Price ₹269000

Your Spending Profile:
- Average monthly spend: ₹6000
- Total historical spend: ₹20000
- Spending is stable

Affordability Check (2 months to save):
- Monthly savings needed: ₹134500
- Your current monthly surplus: ₹-128500

Recommendation:
❌ Currently tight. You'd need to save ₹134500/month, but currently 
spend ₹6000/month. You can afford it in about 45 months if you:
  1. Cut unnecessary expenses by ₹128500/month
  2. Redirect that towards savings
  3. Or wait 45 months and buy from regular savings

Action Steps:
1. Track discretionary spending (dining out, entertainment)
2. Set automatic savings of ₹134500 per month
3. Monitor progress monthly
```

### Example 4: Financial Advice
**You ask**: `Give me financial advice`

**AI responds**:
```
Your Financial Overview:

📊 Spending Summary:
- Total spend: ₹20000
- Average monthly: ₹6667
- Data period: 3 months
- Spending is stable, changing by about ₹0 per month

Top Spending Categories:
1. Food: ₹8500 (42.5%)
2. Utilities: ₹7500 (37.5%)
3. Transport: ₹2100 (10.5%)
4. Entertainment: ₹1800 (9.0%)

⚠️ Overspending Alerts:
High spending detected in Food: 42.50%

💡 Savings Opportunities:
1. Reduce Food by 15% → Save ₹1275
2. Reduce Utilities by 15% → Save ₹1125
3. Reduce Transport by 15% → Save ₹315

✅ Recommendations:
1. Focus on the top 3 categories for cost reduction
2. Set monthly budget 10-15% below current average (₹5666-5900)
3. Track discretionary vs essential spending separately
```

### Example 5: Forecasting
**You ask**: `Forecast my spending for next month`

**AI responds**:
```
Spending forecast for the next 6 months:
2026-04: ₹6500
2026-05: ₹6750
2026-06: ₹7000
2026-07: ₹7250
2026-08: ₹7500
2026-09: ₹7750
```

---

## 🛠️ Troubleshooting

### No responses from AI?
1. Check `.env` file has `GROQ_API_KEY`
2. Verify API key is valid (check Groq console)
3. Check internet connection

### Slow on first run?
1. First time generates embeddings (2-5 seconds)
2. Subsequent runs are cached (fast)
3. If still slow, reduce data size

### "No spending data" error?
1. Ensure CSV has data for that month
2. Check date format is recognizable
3. Try different date formats

---

## 📚 Learn More

- Full documentation: [README.md](README.md)
- System design: [ARCHITECTURE.md](ARCHITECTURE.md)
- All examples: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)

---

## 🎯 Next Steps

1. ✅ Upload your real expense data
2. ✅ Explore the dashboard
3. ✅ Ask purchase planning questions
4. ✅ Get financial advice
5. ✅ Plan future purchases

Enjoy smarter financial management! 💰
