from data_loader import load_data
from embedder import create_embeddings, model
from ai_service import generate_answer
from rag_engine import VectorDB
from groq import Groq
from dotenv import load_dotenv
import os

# load_dotenv()
# # 🔑 Add your Groq API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load data
documents, all_data = load_data("expense.xlsx")

# Create embeddings
embeddings = create_embeddings(documents)

# Create vector DB
db = VectorDB(embeddings, documents)

while True:
    query = input("👉 Ask: ")
    answer = generate_answer(query, db, all_data)
    print("\n💡 Answer:\n", answer)
