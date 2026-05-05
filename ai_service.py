from groq import Groq
from embedder import model
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer_with_memory(query, db, all_data, history=""):
    
    query_embedding = model.encode([query])
    results = db.search(query_embedding, k=50)

    context = "\n".join(results)

    summary = f"""
    Total records: {len(all_data)}
    Date range: {all_data['date'].min()} to {all_data['date'].max()}
    Total spend: ₹{all_data['price'].sum()}
    """

    prompt = f"""
    You are a financial analyst.

    IMPORTANT:
    - The dataset is complete.
    - Do NOT assume missing data.

    DATA SUMMARY:
    {summary}

    Conversation history:
    {history}

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

    return response.choices[0].message.content