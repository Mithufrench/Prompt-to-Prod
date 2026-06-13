// API Base URL - Update this to your actual API endpoint
const API_BASE_URL = window.location.origin.includes('localhost') 
    ? 'http://localhost:8000' 
    : 'https://prompt-to-prod-production.railway.app';

// Navigation active link highlighting
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// Chat functionality
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;

    // Add user message to chat
    addMessageToChat(message, 'user');
    input.value = '';

    try {
        // Send to AI API
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message })
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const data = await response.json();
        addMessageToChat(data.response, 'bot');
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('Sorry, I encountered an error. Please try again.', 'bot');
    }
}

function addMessageToChat(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(message)}</div>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Allow sending message with Enter key
document.getElementById('chat-input')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Check Health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        const statusBadge = document.getElementById('api-status');
        const healthBadge = document.getElementById('health-status');
        const versionBadge = document.getElementById('version-status');
        
        statusBadge.textContent = '● Online';
        statusBadge.className = 'status-badge status-online';
        
        healthBadge.textContent = '● Healthy';
        healthBadge.className = 'status-badge status-healthy';
        
        versionBadge.textContent = data.version || '2.0.0';
        
        alert('✅ API is healthy and responding!\n\n' + JSON.stringify(data, null, 2));
    } catch (error) {
        console.error('Health check failed:', error);
        alert('❌ API is offline or unreachable');
        document.getElementById('api-status').textContent = '● Offline';
        document.getElementById('api-status').className = 'status-badge status-offline';
    }
}

// Get Metrics
async function getMetrics() {
    try {
        const response = await fetch(`${API_BASE_URL}/metrics`);
        const data = await response.json();
        alert('📊 Current Metrics:\n\n' + JSON.stringify(data, null, 2));
    } catch (error) {
        console.error('Failed to fetch metrics:', error);
        alert('❌ Could not fetch metrics');
    }
}

// Open API Docs
function openAPIDocs() {
    window.open(`${API_BASE_URL}/docs`, '_blank');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Check health on load
    checkHealth();
    
    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Hamburger menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
        });
    }
});

// Add some example questions for the AI
const exampleQuestions = [
    "How do I deploy with Kubernetes?",
    "What is Docker?",
    "How do I use Terraform?",
    "What is CI/CD?",
    "How do I optimize my infrastructure?"
];

// Function to get a random example question
function getExampleQuestion() {
    return exampleQuestions[Math.floor(Math.random() * exampleQuestions.length)];
}

// Auto-initialize chat with welcome message
window.addEventListener('load', () => {
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages.children.length === 1) {
        const exampleBtn = document.createElement('div');
        exampleBtn.className = 'message bot-message';
        exampleBtn.innerHTML = `
            <div class="message-content">
                <p>Example: "${getExampleQuestion()}"</p>
            </div>
        `;
        // Don't auto-add, let user interact first
    }
});
