from data_loader import load_data
from embedder import create_embeddings, model
from rag_engine import VectorDB
from groq import Groq
from dotenv import load_dotenv
import os

# load_dotenv()
# # 🔑 Add your Groq API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))/

# Load data
documents, all_data = load_data("expense.xlsx")

# Create embeddings
embeddings = create_embeddings(documents)

# Create vector DB
db = VectorDB(embeddings, documents)

summary = f"""
Total records: {len(all_data)}
Date range: {all_data['date'].min()} to {all_data['date'].max()}
Total spend: ₹{all_data['price'].sum()}
"""

print("💡 RAG System Ready! Ask your questions.\n")

while True:
    query = input("👉 Ask: ")

    # ✅ Convert query to embedding
    query_embedding = model.encode([query])

    # ✅ Search using embedding
    results = db.search(query_embedding, k=50)

    context = "\n".join(results)

    prompt = f"""
You are a financial analyst.

IMPORTANT:
- The dataset is complete.
- Do NOT assume missing data.
- Do NOT complain about data quality.
- Answer ONLY based on given data.

DATA SUMMARY:
{summary}

SAMPLE DATA:
{context}

Question: {query}

Give:
1. Clear insights
2. Spending patterns
3. Practical suggestions
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    print("\n💡 Answer:\n", response.choices[0].message.content)