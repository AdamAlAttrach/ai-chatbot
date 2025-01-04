from langchain_groq import ChatGroq
import os
from sql_llm import generate_query
import sqlite3
import pandas as pd
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

api_key = os.getenv('GROQ_API_KEY')
llm = ChatGroq(api_key=api_key)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


df = pd.read_csv('vehicles.csv')
conn = sqlite3.connect('cars.db')
df.to_sql('cars', conn, index=False, if_exists='replace')
conn.close()

system = (
    "You are Torero, a professional and friendly car dealership agent. Your goal is to assist customers with their car-related inquiries and present information in a clear, concise, and engaging way."
    "Use conversational language to make the experience enjoyable."
    "Make your answers more in a bullet point format."
    "Only provide the information that is relevant to the user's query."
)   
human = (
    "User input: {user_input}"
    "Matches from the databse"
    "{search_results}\n"
    "Use the matches to provide a conversational and context-aware response to the user."
)

template = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", human)
])

chain = template | llm


def handle_customer_request(user_prompt):
    """End-to-end handling of the customer's request."""
    # Generate SQL query
    query = generate_query(user_prompt)
    print("Generated Query:", query)

    try:
        conn = sqlite3.connect('cars.db')
        filtered_df = pd.read_sql_query(query, conn)
        conn.close()
        
        texts = filtered_df["description"].tolist()
        metadata = filtered_df.drop(columns=["description"]).to_dict(orient="records")
        vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadata)
    except Exception as e:
            texts = df["description"].tolist()
            metadata = df.drop(columns=["description"]).to_dict(orient="records")

            vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadata)
    search_results = vectorstore.similarity_search(user_prompt, k=3)

    formatted_results = "\n".join(
        f"{i+1}. {result.page_content}"
        for i, result in enumerate(search_results)
    )

    response = chain.invoke({
        "search_results": formatted_results,
        "user_input": user_prompt
    })

    print(f"\nAssistant: {response.content}")
    return response.content


# Example usage
user_prompt = "Show me all cars priced above $20,000."
response = handle_customer_request(user_prompt)
print(response)