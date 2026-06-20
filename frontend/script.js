// Enhanced AI Agent Frontend with Multi-Agent Support

const API_BASE = window.location.origin;
let conversationHistory = [];
let selectedAgent = 'devops_expert';

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Frontend initialized');
    initializeUI();
    loadAgents();
    checkHealth();
});

function initializeUI() {
    // Add enter key handler for chat input
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
}

// ==================== API CALLS ====================

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        console.log('✅ Health check:', data);
        updateHealthUI(data);
        
        return data;
    } catch (error) {
        console.error('❌ Health check failed:', error);
        updateHealthUI({ status: 'error' });
    }
}

async function getMetrics() {
    try {
        const response = await fetch(`${API_BASE}/metrics`);
        const data = await response.json();
        
        console.log('📊 Metrics:', data);
        updateMetricsUI(data);
        
        return data;
    } catch (error) {
        console.error('❌ Metrics failed:', error);
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const query = input.value.trim();
    
    if (!query) return;
    
    // Add user message to chat
    addMessageToChat('user', query);
    input.value = '';
    
    // Get recommended agent
    const agent = await recommendAgent(query);
    selectedAgent = agent || 'devops_expert';
    
    // Send to AI
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                agent_type: selectedAgent,
                conversation_history: conversationHistory
            })
        });
        
        const data = await response.json();
        
        // Add to conversation history
        conversationHistory.push({
            role: 'user',
            content: query
        });
        
        conversationHistory.push({
            role: 'assistant',
            content: data.response
        });
        
        // Add bot response to chat
        addMessageToChat('bot', data.response, data.agent_type);
        
    } catch (error) {
        console.error('❌ Chat error:', error);
        addMessageToChat('bot', '❌ Error: ' + error.message);
    }
}

async function sendStreamingMessage() {
    const input = document.getElementById('chat-input');
    const query = input.value.trim();
    
    if (!query) return;
    
    addMessageToChat('user', query);
    input.value = '';
    
    try {
        const response = await fetch(`${API_BASE}/chat/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                agent_type: selectedAgent,
                conversation_history: conversationHistory
            })
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        const messageBubble = addMessageToChat('bot', '', selectedAgent);
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    if (data.chunk) {
                        fullResponse += data.chunk;
                        messageBubble.querySelector('.message-content').textContent = fullResponse;
                    }
                }
            }
        }
        
        // Add to conversation history
        conversationHistory.push({ role: 'user', content: query });
        conversationHistory.push({ role: 'assistant', content: fullResponse });
        
    } catch (error) {
        console.error('❌ Streaming error:', error);
        addMessageToChat('bot', '❌ Error: ' + error.message);
    }
}

async function designArchitecture() {
    const projectType = prompt('Project type (e.g., web_app, microservices, data_pipeline):');
    const requirements = prompt('Requirements:');
    const constraints = prompt('Constraints (optional):');
    
    if (!projectType || !requirements) return;
    
    try {
        const response = await fetch(`${API_BASE}/architecture/design`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_type: projectType,
                requirements: requirements,
                constraints: constraints
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            addMessageToChat('bot', '🏗️ Architecture Design:\n\n' + data.architecture);
        } else {
            addMessageToChat('bot', '❌ Error: ' + data.message);
        }
        
    } catch (error) {
        console.error('❌ Architecture error:', error);
        addMessageToChat('bot', '❌ Error: ' + error.message);
    }
}

async function recommendAgent(query) {
    try {
        const response = await fetch(`${API_BASE}/agents/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        console.log('🧠 Recommended agent:', data.recommended_agent);
        
        return data.recommended_agent;
        
    } catch (error) {
        console.error('❌ Agent recommendation error:', error);
        return 'devops_expert';
    }
}

async function loadAgents() {
    try {
        const response = await fetch(`${API_BASE}/agents`);
        const data = await response.json();
        
        console.log('🧠 Available agents:', data.agents);
        updateAgentsUI(data.agents);
        
    } catch (error) {
        console.error('❌ Failed to load agents:', error);
    }
}

async function testEndpoint(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        const data = await response.json();
        
        console.log(`✅ ${endpoint}:`, data);
        alert('Endpoint working! Check console for details.');
        
    } catch (error) {
        console.error(`❌ ${endpoint} error:`, error);
        alert('Endpoint failed: ' + error.message);
    }
}

// ==================== UI UPDATES ====================

function addMessageToChat(role, content, agent = null) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    let agentLabel = '';
    if (agent && role === 'bot') {
        agentLabel = `<span class="agent-label">[${agent.replace(/_/g, ' ')}]</span>`;
    }
    
    messageDiv.innerHTML = `
        <div class="message-header">${agentLabel}</div>
        <div class="message-content">${escapeHtml(content)}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

function updateHealthUI(data) {
    const statusBadge = document.getElementById('status-badge');
    const healthBadge = document.getElementById('health-badge');
    const versionText = document.getElementById('version-text');
    
    if (statusBadge) {
        statusBadge.className = data.status === 'healthy' ? 'badge badge-online' : 'badge badge-offline';
        statusBadge.textContent = data.status === 'healthy' ? '● Online' : '● Offline';
    }
    
    if (healthBadge) {
        healthBadge.className = data.status === 'healthy' ? 'badge badge-healthy' : 'badge badge-error';
        healthBadge.textContent = data.status === 'healthy' ? '● Healthy' : '● Error';
    }
    
    if (versionText) {
        versionText.textContent = data.version || '2.0.0';
    }
}

function updateMetricsUI(data) {
    const requests = document.getElementById('metric-requests');
    const errors = document.getElementById('metric-errors');
    const status = document.getElementById('metric-status');
    
    if (requests) requests.textContent = data.agent_requests_total || 0;
    if (errors) errors.textContent = data.agent_errors_total || 0;
    if (status) status.textContent = data.agent_status || 'Unknown';
}

function updateAgentsUI(agents) {
    // Dynamically add agent buttons if needed
    const actionsPanel = document.querySelector('.actions-panel');
    if (actionsPanel && agents.length > 0) {
        console.log('Available agents:', agents);
    }
}

// ==================== UTILITY FUNCTIONS ====================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function askAI(query) {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.value = query;
        sendMessage();
    }
}

function testAPI() {
    checkHealth();
    setTimeout(() => {
        askAI('What is Kubernetes?');
    }, 1000);
}

function scrollTo(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function openDocs() {
    const docsSection = document.getElementById('docs');
    if (docsSection) {
        docsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function handleHeroPromptEnter(event) {
    if (event.key === 'Enter') {
        sendHeroPrompt();
    }
}

function sendHeroPrompt() {
    const input = document.getElementById('hero-prompt-input');
    if (input) {
        const query = input.value.trim();
        if (query) {
            scrollTo('dashboard');
            setTimeout(() => {
                const chatInput = document.getElementById('chat-input');
                if (chatInput) {
                    chatInput.value = query;
                    sendMessage();
                }
            }, 500);
        }
    }
}

// ==================== AUTO-REFRESH ====================

// Refresh health and metrics every 30 seconds
setInterval(() => {
    checkHealth();
    getMetrics();
}, 30000);

console.log('✅ Enhanced AI Frontend loaded with:');
console.log('  - Multi-agent AI system');
console.log('  - Conversation history');
console.log('  - Streaming responses');
console.log('  - Agent recommendation');
console.log('  - Architecture design');
