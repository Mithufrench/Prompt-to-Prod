"""
Lightweight AI Agent with FastAPI
No external API dependencies required
"""
from fastapi import FastAPI
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Agent API", version="2.0.0")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    status: str = "success"

# Simple responses (no LLM needed)
def process_query(query: str) -> str:
    """Process user query with simple logic"""
    query_lower = query.lower()
    
    if "hello" in query_lower or "hi" in query_lower:
        return "Hello! I'm an AI assistant. How can I help?"
    elif "math" in query_lower or "calculate" in query_lower:
        return "I can help with math calculations. Try: 2 + 2"
    elif "terraform" in query_lower:
        return "I can help with Terraform infrastructure. Ask me anything!"
    elif "kubernetes" in query_lower:
        return "I can help with Kubernetes deployments and commands."
    else:
        return f"You asked: {query}. I'm ready to assist with DevOps tasks!"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai-agent", "version": "2.0.0"}

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Chat with AI agent"""
    try:
        logger.info(f"Query: {request.query}")
        response = process_query(request.query)
        return QueryResponse(response=response, status="success")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return QueryResponse(response=f"Error: {str(e)}", status="error")

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return {
        "agent_requests_total": 0,
        "agent_errors_total": 0,
        "agent_status": "running"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Agent API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "POST /chat": "Chat with AI agent",
            "GET /health": "Health check",
            "GET /metrics": "Prometheus metrics",
            "GET /docs": "API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Agent API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
