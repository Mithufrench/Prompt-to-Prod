"""
LangChain-based AI Agent with FastAPI
Simplified version for Railway deployment
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Agent API", version="2.0.0")

# Initialize LLM
try:
    llm = OpenAI(temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    logger.warning(f"LLM initialization: {e}")
    llm = None

# Memory for conversation context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define tools
def search_tool(query: str) -> str:
    """Simulated search tool"""
    return f"Search results for: {query}"

def math_tool(expression: str) -> str:
    """Simulated math tool"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def terraform_tool(command: str) -> str:
    """Simulated Terraform execution"""
    return f"Terraform would execute: {command}"

def kubernetes_tool(action: str) -> str:
    """Simulated Kubernetes action"""
    return f"Kubernetes action: {action}"

tools = [
    Tool(
        name="Search",
        func=search_tool,
        description="Search for information"
    ),
    Tool(
        name="Calculator",
        func=math_tool,
        description="Perform math calculations"
    ),
    Tool(
        name="Terraform",
        func=terraform_tool,
        description="Execute Terraform commands for infrastructure"
    ),
    Tool(
        name="Kubernetes",
        func=kubernetes_tool,
        description="Execute Kubernetes commands"
    ),
]

# Initialize agent
agent = None
if llm:
    try:
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
            max_iterations=3,
        )
    except Exception as e:
        logger.warning(f"Agent initialization: {e}")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai-agent", "version": "2.0.0"}

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Chat with AI agent"""
    try:
        if not agent:
            return QueryResponse(response="AI agent not initialized. Check OpenAI API key.")
        
        logger.info(f"Query: {request.query}")
        response = agent.run(request.query)
        return QueryResponse(response=response)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return QueryResponse(response=f"Error: {str(e)}")

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
