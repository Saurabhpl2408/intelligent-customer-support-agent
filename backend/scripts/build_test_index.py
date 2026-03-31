from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="Refunds are processed within 5-7 business days.", metadata={"source": "refund_policy.md"}),
    Document(page_content="Free shipping on orders over $50.", metadata={"source": "shipping_faq.md"}),
    Document(page_content="To reset your password, click 'Forgot Password' on the login page.", metadata={"source": "account_faq.md"}),
    Document(page_content="Our return window is 30 days from the delivery date.", metadata={"source": "return_policy.md"}),
    Document(page_content="We accept Visa, Mastercard, PayPal, and Apple Pay.", metadata={"source": "payment_faq.md"}),
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = FAISS.from_documents(docs, embeddings)
store.save_local("vectorstore/faiss_index")
print(f"Index saved with {store.index.ntotal} vectors")