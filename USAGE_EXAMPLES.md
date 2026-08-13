# Usage Examples - Financer AI

Comprehensive guide with real-world examples and expected outputs.

---

## 1. Basic Spending Queries

### Example 1.1: Total Lifetime Spending
**Query**: `How much have I spent in total?`

**System Intent**: TOTAL_SPEND

**Response**:
```
Your total spending is ₹20000

This covers your entire spending history across all months and categories.
```

---

### Example 1.2: Monthly Spending
**Query**: `What did I spend in January 2026?`

**System Intent**: MONTHLY_SPEND

**Response**:
```
Your spending in January 2026 is ₹5150

Breakdown:
- Food: ₹1550
- Transport: ₹500
- Utilities: ₹2000
- Entertainment: ₹1100
```

---

### Example 1.3: Specific Date Range
**Query**: `How much did I spend from 1st to 15th of January?`

**System Intent**: DATE_SPEND

**Response**:
```
Your spending from 2026-01-01 to 2026-01-15 is ₹2600

Transactions:
- Jan 5: ₹1200 (Food)
- Jan 6: ₹350 (Food)
- Jan 7: ₹500 (Transport)
- Jan 8: ₹2000 (Utilities) [Outside range]
```

---

## 2. Category Analysis

### Example 2.1: Top Spending Categories
**Query**: `Which categories do I spend the most on?`

**System Intent**: TOP_CATEGORY_SPEND

**Response**:
```
Top 5 spending categories:
1. Food: ₹8500 (42.5%)
2. Utilities: ₹7500 (37.5%)
3. Transport: ₹2100 (10.5%)
4. Entertainment: ₹1800 (9.0%)
5. Healthcare: ₹100 (0.5%)
```

---

### Example 2.2: Single Category Details
**Query**: `How much do I spend on food?`

**System Intent**: CATEGORY_SPEND

**Response**:
```
Total food spending: ₹8500

Monthly breakdown:
- January: ₹1550
- February: ₹2400
- March: ₹4550

Recent food expenses:
- Mar 25: ₹800 (Restaurant)
- Mar 18: ₹1900 (Groceries)
- Mar 7: ₹500 (Restaurant)
- Mar 3: ₹1300 (Groceries)
- Feb 20: ₹700 (Restaurant)
```

---

## 3. Purchase Planning (NEW)

### Example 3.1: Can I Afford a Bike?
**Query**: `Can I buy a Royal Enfield Meteor bike which is 269000 rupees in August 2026?`

**System Intent**: PURCHASE_ADVICE

**Response**:
```
Purchase Analysis: Item Price ₹269000

Your Spending Profile:

Average monthly spend: ₹25029
Total historical spend: ₹1076252
Spending is increasing, changing by about ₹815.46 per month over the last 6 months.
Affordability Check (1 month to save):

Monthly savings needed: ₹269000
Your current monthly surplus: ₹-243970
Recommendation: ❌ Currently tight. You'd need to save ₹269000/month, but currently spend ₹25029/month. You can afford it in about 11 months if you:

Cut unnecessary expenses by ₹243970/month
Redirect that towards savings
Or wait 11 months and buy from regular savings
Action Steps:

Track discretionary spending (dining out, entertainment)
Set automatic savings of ₹269000 per month
Monitor progress monthly
```

---

### Example 3.2: Laptop Purchase Planning
**Query**: `How much do I need to save for a 50000 rupee laptop?`

**System Intent**: PURCHASE_ADVICE

**Response**:
```
**Purchase Analysis: Item Price ₹50000**

**Your Spending Profile:**
- Average monthly spend: ₹6667
- Total historical spend: ₹20000
- Spending trend: Stable

**Affordability Check (1 month from now):**
- Monthly savings needed: ₹50000
- Your current monthly surplus: ₹-43333

**Recommendation:**
✅ **Feasible but tight.** You can afford this in ~7.5 months by:

1. **Next month (realistic):**
   - Cut 50% of non-essential spending
   - Redirect to savings

2. **Better option (8 months):**
   - Cut 20% of current spending
   - Maintain lifestyle while saving

**Action Steps:**
1. Set savings goal: ₹7000/month for 8 months
2. Cut top category (Food: ₹8500) by 20% → Save ₹1700
3. Cut utilities by 10% → Save ₹750
4. Cut entertainment by 50% → Save ₹900
5. Total monthly savings: ₹3350
```

---

## 4. Financial Advice (NEW)

### Example 4.1: General Financial Guidance
**Query**: `Give me financial advice`

**System Intent**: FINANCIAL_ADVICE

**Response**:
```
**Your Financial Overview:**

📊 **Spending Summary:**
- Total spend: ₹20000
- Average monthly: ₹6667
- Data period: January to March 2026 (3 months)
- Spending trend: Stable ➡️

**Top 5 Spending Categories:**
1. Food: ₹8500 (42.5%)
2. Utilities: ₹7500 (37.5%)
3. Transport: ₹2100 (10.5%)
4. Entertainment: ₹1800 (9.0%)
5. Healthcare: ₹100 (0.5%)

**⚠️ Overspending Alerts:**
- High spending detected in **Food**: 42.50% of total
  (Benchmark: 30-35% is healthy)

💡 **Savings Opportunities:**
1. Reduce **Food** by 15% → Save ₹1275/month
2. Reduce **Utilities** by 15% → Save ₹1125/month
3. Reduce **Transport** by 15% → Save ₹315/month
   **Total monthly savings: ₹2715**

✅ **Recommendations:**
1. **Short-term (This month):**
   - Cook at home 2x per week instead of eating out
   - Review utility bills for optimization
   - Carpool or use public transport 2x per week

2. **Medium-term (Next 3 months):**
   - Build emergency fund: 3x monthly spend = ₹20000
   - Set spending budget: ₹6000/month (10% reduction)
   - Track categories weekly

3. **Long-term (Next 6-12 months):**
   - Automate savings: ₹2000/month to savings account
   - Plan major purchases (bike, laptop) with 6+ month timeline
   - Review and optimize budget quarterly

4. **Behavioral Changes:**
   - Use app to track daily, not monthly
   - Set category limits in your mind
   - Review spending with friends for accountability
```

---

### Example 4.2: Savings Potential
**Query**: `How can I increase my savings?`

**System Intent**: FINANCIAL_ADVICE

**Response**:
```
**Savings Potential Analysis:**

**Current Situation:**
- Monthly Income (assumed): Unknown (share for better analysis)
- Monthly Spend: ₹6667
- Potential Savings: ₹X (Need income info)

**Savings Opportunities Identified:**

💰 **Quick Wins (0-1 week):**
1. **Reduce dining out** 
   - Current: ~₹800/month
   - Target: ₹400/month
   - Savings: ₹400/month

2. **Entertainment cuts**
   - Current: ₹1800/month
   - Target: ₹900/month (remove subscriptions)
   - Savings: ₹900/month

3. **Negotiate utilities**
   - Current: ₹7500/month
   - Target: ₹6750/month (shop for better plans)
   - Savings: ₹750/month

   **Quick Total: ₹2050/month**

📈 **Sustainable Changes (1-3 months):**
- Automate transfers to savings account
- Reduce food waste (grocery planning)
- Shift to less expensive transportation
- Cancel unused subscriptions

📊 **Projected Impact:**
- Current monthly savings rate: 0%
- With changes: 20-30% savings rate
- In 12 months: ₹16000-24000 saved
- Emergency fund achievable in 8-10 months
```

---

## 5. Spending Forecasts

### Example 5.1: 6-Month Forecast
**Query**: `Forecast my spending for the next 6 months`

**System Intent**: FORECAST

**Response**:
```
**6-Month Spending Forecast:**

Analyzing your trend from January to March 2026...
Current trend: **Stable** (±0% monthly change)

**Forecast:**
- April 2026: ₹6667 (Stable)
- May 2026: ₹6667 (Stable)
- June 2026: ₹6667 (Stable)
- July 2026: ₹6667 (Stable)
- August 2026: ₹6667 (Stable)
- September 2026: ₹6667 (Stable)

**Analysis:**
Your spending has been consistent at ~₹6667/month. With no major 
planned changes, expect similar levels going forward.

**Note:** If you make the recommended cuts, forecast would be ~₹5900/month.
```

---

### Example 5.2: Seasonal Trends
**Query**: `What's my spending trend?`

**System Intent**: FINANCIAL_ADVICE (with trend analysis)

**Response**:
```
**Spending Trend Analysis:**

📈 **Monthly Change:**
- January 2026: ₹5150
- February 2026: ₹5900
- March 2026: ₹9050
- Overall trend: **Increasing** (+76% over 3 months)

**What's causing the increase:**
- Food expenses rose 193% (₹1550 → ₹4550)
- Utilities remained stable
- New category (Healthcare) appeared in March

**Outlook:**
⚠️ If this trend continues, monthly spending will reach ₹12500 by June 2026.

**Recommendations:**
1. Investigate food spending spike in March
2. Review one-time vs recurring expenses
3. Implement budget controls to limit growth
4. Plan for increased spending in budgeting
```

---

## 6. Complex Scenarios

### Example 6.1: Multi-Purchase Planning
**Query**: `I want to save 500000 for a laptop AND 269000 for a bike. Can I do it?`

**System Intent**: RAG (fallback to LLM)

**Response**:
```
**Multi-Purchase Savings Plan:**

Total needed: ₹769000
Current monthly savings: ₹0 (100% of budget spent)

**Option 1: Sequential Purchases**
- Buy laptop first (₹500000):
  - Timeline: ~75 months (6+ years)
  - Monthly savings needed: ₹6667
  
- Then buy bike (₹269000):
  - Additional timeline: 40 months
  - Total: 115 months

❌ Not practical - too long

**Option 2: Parallel Savings**
- Save for both simultaneously
- Total needed: ₹769000
- Timeline: 115 months at current spend
- Monthly savings target: ₹6671

❌ Still not practical

**Realistic Scenario:**
1. Increase income or reduce expenses by 50%
2. With ₹3333 monthly savings (50% budget cut):
   - Save ₹500000 in 150 months (laptop)
   - Save ₹269000 in 81 months (bike)
   
✅ Achievable in ~4-5 years with discipline

**Better Approach:**
1. Set milestone: Year 1 = Laptop (₹500000)
2. Emergency fund first (₹20000)
3. Year 2-3 = Bike (₹269000)
4. Both achievable with 30% budget reduction
```

---

### Example 6.2: Category Deep Dive
**Query**: `Show me detailed food spending analysis`

**System Intent**: CATEGORY_SPEND + RAG

**Response**:
```
**Food Spending Deep Dive:**

**Total: ₹8500 (42.5% of budget)**

**Monthly Breakdown:**
| Month | Amount | # Transactions |
|-------|--------|-----------------|
| Jan   | ₹1550  | 2               |
| Feb   | ₹2400  | 2               |
| Mar   | ₹4550  | 4               |
| Total | ₹8500  | 8               |

**Expense Type:**
- Groceries: ₹4000 (47%)
- Restaurant: ₹3500 (41%)
- Misc: ₹1000 (12%)

**Top Transactions:**
1. Mar 18: ₹1900 Groceries
2. Mar 3: ₹1300 Groceries
3. Mar 25: ₹800 Restaurant
4. Feb 15: ₹1800 Groceries
5. Feb 5: ₹450 Restaurant

**Pattern Observed:**
- Groceries increasing (Feb: ₹1250, Mar: ₹2750)
- Restaurant spending stable (₹350-400/month)
- March spike: +90% vs Feb

**Recommendations:**
1. Review what changed in March
2. Stabilize around ₹7000/month (₹233/day)
3. Meal plan to reduce grocery waste
4. Restaurant frequency seems controlled ✓
```

---

## 7. Error Handling Examples

### Example 7.1: Invalid Query
**Query**: `When is my birthday?`

**System Intent**: RAG (unrecognized)

**Response**:
```
I don't have information about your personal events like birthdays.

I can help with:
- Spending analysis (total, by month, by category)
- Purchase planning (affordability checks)
- Financial advice (savings strategies)
- Forecasting (future spending)

Try asking: "How much did I spend on gifts?"
```

---

### Example 7.2: Missing Data
**Query**: `How much did I spend in December 2025?`

**System Intent**: DATE_SPEND (no data)

**Response**:
```
I don't have spending data for December 2025.

Available data period: January 2026 - March 2026

Please choose from:
- January 2026: ₹5150
- February 2026: ₹5900
- March 2026: ₹9050

Or upload older data to expand your analysis range.
```

---

## 8. Tips for Best Results

### ✅ DO:
- Be specific: "Food in March" not just "food"
- Use actual rupee amounts: "₹50000 laptop"
- Mention timeframe: "August 2026" or "next month"
- Ask follow-ups: "Why is food high?" → "What can I cut?"

### ❌ DON'T:
- Ask about non-financial topics
- Use vague amounts: "Some bike"
- Forget to mention dates for forecasts
- Ask multiple questions at once

### 💡 PRO TIPS:
1. Upload 6+ months of data for better insights
2. Categorize consistently (same category names)
3. Use purchase planning before big purchases
4. Check affordability suggestions before buying
5. Review quarterly forecasts to adjust budget

---

## Summary: Query Types

| Query Type | Example | Intent | Speed |
|-----------|---------|--------|-------|
| Total Spending | "Total spend?" | TOTAL_SPEND | ⚡ Fast |
| Monthly | "January spending?" | MONTHLY_SPEND | ⚡ Fast |
| Date Range | "1st-15th January?" | DATE_SPEND | ⚡ Fast |
| Top Categories | "Top spending?" | TOP_CATEGORY_SPEND | ⚡ Fast |
| Category Detail | "Food spending?" | CATEGORY_SPEND | ⚡ Fast |
| Purchase Plan | "Can I buy bike?" | PURCHASE_ADVICE | ⚡ Fast |
| Forecast | "Future spending?" | FORECAST | ⚡ Fast |
| Advice | "Financial advice?" | FINANCIAL_ADVICE | 🧠 Smart |
| Open-ended | "Show patterns?" | RAG | 🧠 Smart |

---

Enjoy exploring your finances! 💰
