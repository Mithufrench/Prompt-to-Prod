from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from groq import Groq
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Prompt-to-Prod AI DevOps Platform")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq Client
groq_client = None

def get_groq_client():
    global groq_client
    if groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY not found! Using fallback responses.")
            return None
        groq_client = Groq(api_key=api_key)
    return groq_client

# Models
class ChatRequest(BaseModel):
    query: str

class HealthResponse(BaseModel):
    status: str
    version: str
    message: str

# System Prompt - Makes AI very DevOps-focused
SYSTEM_PROMPT = """
You are an expert DevOps Engineer and AI Assistant for "Prompt-to-Prod" platform.
Your goal is to help users with real, production-grade DevOps solutions.

Core strengths:
- Generate complete CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)
- Write Terraform / OpenTofu IaC code
- Create Dockerfiles and docker-compose files
- Generate Kubernetes manifests (Deployment, Service, Ingress, Helm charts)
- Give security best practices, monitoring (Prometheus + Grafana), logging
- Explain concepts clearly with examples

Always be helpful, concise, and provide copy-paste ready code when possible.
Use markdown formatting for readability.
"""

@app.get("/health")
async def health():
    return HealthResponse(
        status="healthy",
        version="2.1.0",
        message="Prompt-to-Prod AI DevOps Platform is running with Groq LLM"
    )

@app.post("/chat")
async def chat(request: ChatRequest):
    start_time = time.time()
    
    client = get_groq_client()
    
    if not client:
        # Fallback if no API key
        return {
            "response": "⚠️ Groq API key is not configured. Please set GROQ_API_KEY environment variable.\n\nIn the meantime, try more specific questions like:\n- Generate a CI/CD pipeline for a Node.js app\n- Write Terraform for an S3 bucket"
        }

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # Excellent balance of speed & quality
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.query}
            ],
            temperature=0.7,
            max_tokens=1200,
            top_p=0.9,
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        logger.info(f"Chat request processed in {time.time() - start_time:.2f}s")
        
        return {"response": response_text}

    except Exception as e:
        logger.error(f"Groq API error: {str(e)}")
        raise HTTPException(status_code=500, detail="AI service temporarily unavailable")

@app.get("/metrics")
async def metrics():
    return {
        "agent_requests_total": 42,
        "agent_errors_total": 0,
        "agent_status": "running",
        "ai_provider": "groq",
        "uptime": "online"
    }

@app.get("/")
async def root():
    return {
        "message": "Welcome to Prompt-to-Prod AI DevOps Platform",
        "docs": "/docs",
        "ai": "Groq Powered"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
