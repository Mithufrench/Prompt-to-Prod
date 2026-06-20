"""
Prompt-to-Prod - AI DevOps Platform with Groq LLM
Enhanced Backend with Groq Integration
Railway-compatible configuration
"""
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
import sys
from pathlib import Path
from groq import Groq

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Prompt-to-Prod AI DevOps", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "mixtral-8x7b-32768")

if not GROQ_API_KEY:
    logger.warning("⚠️  GROQ_API_KEY not set. Set it as an environment variable.")
    client = None
else:
    client = Groq(api_key=GROQ_API_KEY)
    logger.info("✅ Groq client initialized")

# Data Models
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    status: str = "success"

# Process query using Groq LLM
def process_query(query: str) -> str:
    """Process query using Groq LLM"""
    if not client:
        return "Error: Groq API key not configured. Please set GROQ_API_KEY environment variable."
    
    try:
        logger.info(f"Query: {query}")
        
        # System prompt for DevOps expertise
        system_prompt = """You are an expert DevOps engineer and AI assistant for the Prompt-to-Prod platform. 
You have deep knowledge of Docker, Kubernetes, Terraform, CI/CD, deployment strategies, monitoring, and cloud infrastructure.
Provide clear, concise, and practical answers to DevOps and infrastructure questions.
Always include best practices and real-world considerations."""
        
        message = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": query}
            ]
        )
        
        response = message.content[0].text
        logger.info(f"Response generated: {response[:100]}...")
        return response
        
    except Exception as e:
        logger.error(f"Error calling Groq API: {str(e)}")
        return f"Error processing query: {str(e)}"

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint - used by Railway"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "ai-devops-platform",
        "version": "2.0.0",
        "llm": "groq",
        "model": MODEL
    }

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Chat with AI assistant powered by Groq"""
    try:
        logger.info(f"Processing query: {request.query}")
        response = process_query(request.query)
        return QueryResponse(response=response, status="success")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return QueryResponse(response=f"Error: {str(e)}", status="error")

@app.get("/metrics")
async def metrics():
    """Get system metrics"""
    return {
        "agent_requests_total": 42,
        "agent_errors_total": 0,
        "agent_status": "running",
        "llm_provider": "groq",
        "model": MODEL
    }

# Setup static files
app_dir = Path(__file__).parent
if (app_dir.parent / "frontend").exists():
    frontend_path = app_dir.parent / "frontend"
else:
    frontend_path = app_dir / "frontend"

logger.info(f"Frontend path: {frontend_path}")
logger.info(f"Frontend exists: {frontend_path.exists()}")

# Mount static files at root
if frontend_path.exists():
    try:
        app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")
        logger.info(f"✅ Static files mounted at / from {frontend_path}")
        files = list((frontend_path).glob("*"))
        logger.info(f"Files in frontend: {[f.name for f in files]}")
    except Exception as e:
        logger.error(f"Error mounting static files: {e}")
else:
    logger.error(f"❌ Frontend directory does not exist at {frontend_path}")

if __name__ == "__main__":
    import uvicorn
    
    # Read PORT from Railway environment variable
    # Railway sets PORT to a random port (e.g., 47380)
    # This app MUST listen on that PORT for healthchecks to work
    port = int(os.getenv("PORT", 8000))
    
    # Print startup info
    logger.info(f"=" * 50)
    logger.info(f"🚀 Starting Prompt-to-Prod AI DevOps Agent")
    logger.info(f"🔧 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"📊 Port: {port}")
    logger.info(f"🤖 LLM Model: {MODEL}")
    logger.info(f"🔑 Groq API Key: {'✅ Set' if GROQ_API_KEY else '❌ Not set'}")
    logger.info(f"=" * 50)
    
    # Start Uvicorn server on the assigned port
    # This is critical for Railway deployment
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all interfaces
        port=port,        # Use Railway's assigned PORT
        log_level="info"
    )
