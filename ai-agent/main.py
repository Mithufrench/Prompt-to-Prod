<<<<<<< HEAD
"""
Prompt-to-Prod - AI DevOps Platform with Advanced Groq LLM Integration
Enhanced AI Agent for Real Architecture Outcomes
"""
from fastapi import FastAPI, WebSocket
from starlette.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
=======

from fastapi import FastAPI, HTTPException
>>>>>>> 192265a81b1452055b63b083d005eda6e7857ec4
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
<<<<<<< HEAD
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict
from groq import Groq
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Prompt-to-Prod AI DevOps", version="3.0.0")
=======
from groq import Groq
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Prompt-to-Prod AI DevOps Platform")
>>>>>>> 192265a81b1452055b63b083d005eda6e7857ec4

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "mixtral-8x7b-32768")

if not GROQ_API_KEY:
    logger.warning("⚠️  GROQ_API_KEY not set. Set it as an environment variable.")
    client = None
else:
    client = Groq(api_key=GROQ_API_KEY)
    logger.info("✅ Groq client initialized with Mixtral 8x7B model")

# ==================== AI SYSTEM PROMPTS ====================

SYSTEM_PROMPTS = {
    "devops_expert": """You are an expert DevOps Engineer and Cloud Architect. Your role is to provide:
1. Production-ready infrastructure designs
2. Best practices for containerization and orchestration
3. CI/CD pipeline recommendations
4. Security and compliance guidance
5. Cost optimization strategies
6. Performance tuning advice

Always provide:
- Specific, actionable recommendations
- Real-world considerations and trade-offs
- Code examples where applicable
- Links to official documentation when relevant
Format responses with clear sections and bullet points.""",

    "architect": """You are a Senior Software Architect specializing in cloud-native applications. Provide:
1. System design and architecture patterns
2. Scalability and performance considerations
3. Data architecture and database design
4. API design and microservices architecture
5. Technology stack recommendations

Focus on:
- Real production scenarios
- Trade-offs between different approaches
- Practical implementation advice
- Best practices from industry leaders
Always include diagrams in text format when helpful.""",

    "kubernetes_expert": """You are a Kubernetes and Container Orchestration Expert. Help with:
1. Kubernetes cluster design and setup
2. Pod deployment and management
3. Service mesh integration (Istio, Linkerd)
4. Monitoring and logging
5. Security policies and RBAC
6. Performance optimization

Provide:
- YAML configurations with explanations
- Troubleshooting guidance
- Production readiness checklists
- Cost optimization tips""",

    "infrastructure_coder": """You are an Infrastructure as Code (IaC) Expert. Specialize in:
1. Terraform configurations for various cloud providers (AWS, GCP, Azure)
2. CloudFormation templates
3. Ansible playbooks
4. ARM (Azure Resource Manager) templates
5. Pulumi Python/Go code

Requirements:
- Production-ready code
- Security best practices
- State management strategies
- Module design patterns
- Testing approaches for IaC""",

    "security_specialist": """You are a Cloud Security and DevSecOps Expert. Provide guidance on:
1. Security architecture and zero-trust design
2. Container and image security
3. Secrets management
4. Network security and firewalls
5. Compliance (GDPR, HIPAA, SOC2, PCI-DSS)
6. Incident response

Include:
- Specific security controls
- Threat models and mitigation
- Tools and technologies
- Audit and monitoring strategies"""
}

# ==================== DATA MODELS ====================

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ConversationHistory(BaseModel):
    messages: List[ChatMessage] = []
    agent_type: str = "devops_expert"

class QueryRequest(BaseModel):
=======
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
>>>>>>> 192265a81b1452055b63b083d005eda6e7857ec4
    query: str
    agent_type: Optional[str] = "devops_expert"
    conversation_history: Optional[List[ChatMessage]] = None

<<<<<<< HEAD
class QueryResponse(BaseModel):
    response: str
    status: str = "success"
    agent_type: str = "devops_expert"
    model: str = MODEL
    tokens_used: Optional[Dict] = None

class ArchitectureRequest(BaseModel):
    """Request for architecture design"""
    project_type: str  # web_app, microservices, data_pipeline, etc
    requirements: str
    constraints: Optional[str] = None
    technologies: Optional[List[str]] = None

class ArchitectureResponse(BaseModel):
    """Response with architecture design"""
    architecture: str
    diagram: str
    components: List[str]
    recommendations: List[str]
    next_steps: List[str]

# ==================== AI PROCESSING FUNCTIONS ====================

def get_system_prompt(agent_type: str) -> str:
    """Get appropriate system prompt for agent type"""
    return SYSTEM_PROMPTS.get(agent_type, SYSTEM_PROMPTS["devops_expert"])

def process_query_with_groq(query: str, agent_type: str = "devops_expert", 
                           conversation_history: Optional[List[ChatMessage]] = None) -> Dict:
    """Process query using Groq with conversation history"""
    if not client:
        return {
            "response": "Error: Groq API key not configured.",
            "status": "error",
            "agent_type": agent_type
        }
    
    try:
        logger.info(f"Processing query with agent: {agent_type}")
        
        # Build messages list including conversation history
        messages = []
        
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add current query
        messages.append({
            "role": "user",
            "content": query
        })
        
        system_prompt = get_system_prompt(agent_type)
        
        # Call Groq API with streaming for better UX
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        )
        
        result_text = response.content[0].text
        logger.info(f"Response generated by {agent_type} agent")
        
        return {
            "response": result_text,
            "status": "success",
            "agent_type": agent_type,
            "model": MODEL,
            "tokens_used": {
                "input": response.usage.input_tokens if hasattr(response, 'usage') else 0,
                "output": response.usage.output_tokens if hasattr(response, 'usage') else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error calling Groq API: {str(e)}")
        return {
            "response": f"Error processing query: {str(e)}",
            "status": "error",
            "agent_type": agent_type
        }

def design_architecture(project_type: str, requirements: str, 
                       constraints: Optional[str] = None) -> Dict:
    """Generate architecture design using AI"""
    if not client:
        return {"status": "error", "message": "Groq not configured"}
    
    try:
        prompt = f"""Design a production-ready architecture for:

Project Type: {project_type}
Requirements: {requirements}
{f'Constraints: {constraints}' if constraints else ''}

Provide a comprehensive architecture including:
1. System architecture overview (describe as ASCII diagram if helpful)
2. Key components and their responsibilities
3. Data flow between components
4. Technology recommendations
5. Scalability approach
6. Monitoring and observability strategy
7. Security considerations
8. Cost optimization tips
9. Deployment strategy
10. Next implementation steps

Format with clear sections and actionable recommendations."""

        response = client.messages.create(
            model=MODEL,
            max_tokens=3000,
            system=SYSTEM_PROMPTS["architect"],
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "status": "success",
            "architecture": response.content[0].text
        }
        
    except Exception as e:
        logger.error(f"Architecture design error: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

# ==================== API ENDPOINTS ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-devops-platform",
        "version": "3.0.0",
        "llm": "groq",
        "model": MODEL,
        "ai_agents": list(SYSTEM_PROMPTS.keys())
    }

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Chat with AI assistant powered by Groq - Single turn"""
    try:
        logger.info(f"Chat request: {request.query[:100]}...")
        
        result = process_query_with_groq(
            query=request.query,
            agent_type=request.agent_type,
            conversation_history=request.conversation_history
        )
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return QueryResponse(
            response=f"Error: {str(e)}",
            status="error",
            agent_type=request.agent_type
        )

@app.post("/chat/stream")
async def chat_stream(request: QueryRequest):
    """Streaming chat endpoint for real-time responses"""
    try:
        if not client:
            return {"error": "Groq not configured"}
        
        logger.info(f"Streaming chat request: {request.query[:100]}...")
        
        messages = []
        if request.conversation_history:
            for msg in request.conversation_history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        messages.append({
            "role": "user",
            "content": request.query
        })
        
        system_prompt = get_system_prompt(request.agent_type)
        
        # Create streaming response
        stream = client.messages.stream(
            model=MODEL,
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        )
        
        async def generate():
            try:
                with stream as s:
                    for text in s.text_stream:
                        yield f"data: {json.dumps({'chunk': text})}\n\n"
            except Exception as e:
                logger.error(f"Stream error: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
        
    except Exception as e:
        logger.error(f"Stream error: {str(e)}")
        return {"error": str(e)}

@app.post("/architecture/design")
async def design_app_architecture(request: ArchitectureRequest):
    """Design architecture for your application"""
    try:
        logger.info(f"Architecture design request for: {request.project_type}")
        
        result = design_architecture(
            project_type=request.project_type,
            requirements=request.requirements,
            constraints=request.constraints
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Architecture error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/agents")
async def list_agents():
    """List available AI agents"""
    return {
        "agents": [
            {
                "type": agent_type,
                "description": f"Agent specialized in {agent_type.replace('_', ' ')}"
            }
            for agent_type in SYSTEM_PROMPTS.keys()
        ]
    }

@app.post("/agents/recommend")
async def recommend_agent(query: QueryRequest):
    """Recommend best agent for the query"""
    try:
        if not client:
            return {"recommended_agent": "devops_expert"}
        
        agent_selector_prompt = """Based on this query, recommend which specialist agent should handle it.
Choose from: devops_expert, architect, kubernetes_expert, infrastructure_coder, security_specialist

Return ONLY the agent type name, nothing else."""

        response = client.messages.create(
            model=MODEL,
            max_tokens=50,
            system=agent_selector_prompt,
            messages=[{"role": "user", "content": query.query}]
        )
        
        recommended = response.content[0].text.strip().lower()
        
        # Validate recommendation
        if recommended not in SYSTEM_PROMPTS:
            recommended = "devops_expert"
        
        return {
            "query": query.query[:100],
            "recommended_agent": recommended,
            "reason": f"This query is best handled by the {recommended} agent"
        }
        
    except Exception as e:
        logger.error(f"Agent recommendation error: {str(e)}")
        return {"recommended_agent": "devops_expert", "error": str(e)}
=======
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
>>>>>>> 192265a81b1452055b63b083d005eda6e7857ec4

@app.get("/metrics")
async def metrics():
    return {
        "agent_requests_total": 0,
        "agent_errors_total": 0,
        "agent_status": "running",
<<<<<<< HEAD
        "llm_provider": "groq",
        "model": MODEL,
        "available_agents": len(SYSTEM_PROMPTS),
        "streaming_enabled": True,
        "conversation_support": True
    }

# ==================== STATIC FILES ====================

app_dir = Path(__file__).parent
if (app_dir.parent / "frontend").exists():
    frontend_path = app_dir.parent / "frontend"
else:
    frontend_path = app_dir / "frontend"

logger.info(f"Frontend path: {frontend_path}")

if frontend_path.exists():
    try:
        app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")
        logger.info(f"✅ Static files mounted at /")
    except Exception as e:
        logger.error(f"Error mounting static files: {e}")

# ==================== STARTUP ====================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"=" * 60)
    logger.info(f"🚀 Starting Prompt-to-Prod AI DevOps Agent v3.0")
    logger.info(f"🔧 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"📊 Port: {port}")
    logger.info(f"🤖 LLM Model: {MODEL}")
    logger.info(f"🔑 Groq API Key: {'✅ Set' if GROQ_API_KEY else '❌ Not set'}")
    logger.info(f"🧠 AI Agents Available: {len(SYSTEM_PROMPTS)}")
    logger.info(f"  - DevOps Expert")
    logger.info(f"  - Software Architect")
    logger.info(f"  - Kubernetes Expert")
    logger.info(f"  - Infrastructure Coder")
    logger.info(f"  - Security Specialist")
    logger.info(f"✨ Features:")
    logger.info(f"  - Multi-agent AI system")
    logger.info(f"  - Conversation history support")
    logger.info(f"  - Streaming responses")
    logger.info(f"  - Architecture design")
    logger.info(f"  - Agent recommendation")
    logger.info(f"=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
=======
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
>>>>>>> 192265a81b1452055b63b083d005eda6e7857ec4
