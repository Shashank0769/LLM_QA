# Hotel Booking Analytics & QA System

## 📌 Project Overview
This project is designed to analyze hotel booking data, extract insights, and provide a **Retrieval-Augmented Question Answering (RAG)** system. It enables users to retrieve key analytics and ask natural language questions about the data.

## 🏗️ Features
- **Data Analytics**: Insights such as revenue trends, cancellation rates, and booking distribution.
- **RAG-based Question Answering**: Users can ask questions about the dataset, and the system retrieves relevant insights.
- **Streamlit UI**: A user-friendly interface to interact with the system.
- **FastAPI Backend**: API to process user queries and fetch analytics.

## 🛠️ Tech Stack
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Embedding Model**: `all-MiniLM-L6-v2` (for semantic search)
- **Database**: CSV-based storage
- **Visualization**: Matplotlib, Seaborn

## 🚀 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/hotel-booking-analytics.git
cd hotel-booking-analytics
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the API
```bash
uvicorn app:app --reload
```
The FastAPI backend will be available at `http://127.0.0.1:8000`

### 4️⃣ Run the Streamlit App
```bash
streamlit run app_ui.py
```
The UI will be accessible at `http://localhost:8501`

## 🔗 API Endpoints
| Method | Endpoint       | Description                         |
|--------|--------------|-------------------------------------|
| `POST` | `/ask`       | Ask a question about hotel data    |
| `GET`  | `/analytics` | Retrieve analytics insights        |

## 🎯 Sample Queries & Expected Answers
### Query: "Show me the highest revenue bookings"
**Response:**
```json
{
  "answer": "Hotel: Resort Hotel, Country: GBR, Revenue: 55.43, Lead Time: 100 days."
}
```

### Query: "What is the cancellation rate?"
**Response:**
```json
{
  "answer": "Cancellation Rate: 37.04%"
}
```

## 📌 Implementation Details & Challenges
- **Semantic Search for QA:** Used `all-MiniLM-L6-v2` to compare user queries with dataset insights.
- **Data Cleaning:** Processed missing values and normalized fields for consistency.
- **Visualization:** Added revenue trends and geographical insights in Streamlit.
- **Challenge:** Ensuring natural language queries return meaningful structured insights.

## Snapshots

![image](https://github.com/user-attachments/assets/bfbe481d-0097-48b9-9c60-19206f6cc261)

## Analytics

![image](https://github.com/user-attachments/assets/c72adc2c-4178-4473-b7cd-dd36370b8b1d)

