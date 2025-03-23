from fastapi import FastAPI
import pandas as pd
import numpy as np
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import os

# Load dataset
file_path = "hotel_bookings.csv"  # Ensure this file exists
df = pd.read_csv(file_path)

# Handle missing values
df.fillna({"children": 0, "country": "Unknown", "agent": 0, "company": 0}, inplace=True)

# Convert date column to datetime
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')

# Compute analytics
cancellation_rate = df['is_canceled'].mean() * 100
country_counts = df['country'].value_counts(normalize=True) * 100
lead_time_distribution = df['lead_time'].describe().to_dict()

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert booking data to text
df['text'] = df.apply(lambda row: f"Booking ID: {row.name}, Hotel: {row['hotel']}, Country: {row['country']}, Revenue: {row['adr']}, Lead Time: {row['lead_time']}", axis=1)

# FAISS index path
FAISS_INDEX_PATH = "faiss_hotel_index.bin"

# Load or create FAISS index
if os.path.exists(FAISS_INDEX_PATH):
    print("Loading existing FAISS index...")
    index = faiss.read_index(FAISS_INDEX_PATH)
else:
    print("Creating new FAISS index...")
    embeddings = model.encode(df['text'].tolist(), show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings, dtype=np.float32))
    faiss.write_index(index, FAISS_INDEX_PATH)

def ask_question(query):
    query_embedding = model.encode([query])  # Convert query to vector

    # Define possible question types
    question_templates = {
        "highest revenue bookings": lambda: df.nlargest(3, "adr")[["hotel", "country", "adr", "lead_time"]].to_dict(orient="records"),
        "average price of a hotel booking": lambda: {"answer": f"The average price of a hotel booking is {df['adr'].mean():.2f}"},
        "total revenue from bookings": lambda: {"answer": f"The total revenue from bookings is {df['adr'].sum():.2f}"},
        "most booked country": lambda: {"answer": f"The most booked country is {df['country'].value_counts().idxmax()}"},
        "cancellation rate": lambda: {"answer": f"The cancellation rate is {df['is_canceled'].mean() * 100:.2f}%"},
    }

    # Convert predefined questions to embeddings
    template_embeddings = model.encode(list(question_templates.keys()))

    # Use FAISS to find the closest match
    index = faiss.IndexFlatL2(template_embeddings.shape[1])
    index.add(np.array(template_embeddings))
    _, closest_match = index.search(np.array(query_embedding), k=1)

    # Get the best-matched question and run its logic
    best_match_question = list(question_templates.keys())[closest_match[0][0]]
    return question_templates[best_match_question]()  # Run the matched function


# Initialize FastAPI
app = FastAPI()

# ✅ Fix 404 Not Found Issue: Add Home Route
@app.get("/")
def home():
    return {"message": "Welcome to the Hotel Booking Analytics API! Available routes: /ask (POST), /analytics (GET)"}

# Search endpoint
class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def query_api(request: QueryRequest):
    response = ask_question(request.question)  # Now response can be a list or dict

    # If response is a list (multiple records)
    if isinstance(response, list):
        answer_list = [
            f"Hotel: {row['hotel']}, Country: {row['country']}, Revenue: {row['adr']}, Lead Time: {row['lead_time']} days."
            for row in response
        ]
        return {"answer": " ".join(answer_list)}

    # If response is a dictionary (single value answer)
    return response



# Analytics endpoint
@app.get("/analytics")
def get_analytics():
    revenue_trends = df.groupby(["arrival_date_year", "arrival_date_month"])["adr"].sum().reset_index()
    revenue_trends.columns = ["year", "month", "revenue"]

    return {
        "cancellation_rate": df["is_canceled"].mean() * 100,
        "top_countries": df["country"].value_counts(normalize=True).head(5).to_dict(),
        "revenue_trends": revenue_trends.to_dict(orient="records"),
        "lead_times": df["lead_time"].tolist()
    }

# Run with: uvicorn app:app --reload
