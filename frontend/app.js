// Screen and form elements
const authScreen = document.getElementById('auth-screen');
const consoleScreen = document.getElementById('console-screen');
const authForm = document.getElementById('auth-form');
const authMessage = document.getElementById('auth-message');
const submitBtn = document.getElementById('submit-btn');

// Tabs toggle elements
const tabLogin = document.getElementById('tab-login');
const tabSignup = document.getElementById('tab-signup');

let currentMode = 'login'; // Can switch to 'signup'

// --- SWITCH BETWEEN LOGIN & SIGNUP VIEWS ---
tabLogin.addEventListener('click', () => {
    currentMode = 'login';
    tabLogin.classList.add('active');
    tabSignup.classList.remove('active');
    submitBtn.innerText = "Sign In";
    authMessage.innerText = "";
});

tabSignup.addEventListener('click', () => {
    currentMode = 'signup';
    tabSignup.classList.add('active');
    tabLogin.classList.remove('active');
    submitBtn.innerText = "Register Account";
    authMessage.innerText = "";
});

// --- HANDLE FORM SUBMISSIONS (LOGIN / SIGNUP) ---
authForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const usernameInput = document.getElementById('username').value;
    const passwordInput = document.getElementById('password').value;
    
    authMessage.innerText = "Connecting...";
    authMessage.style.color = "#fbbf24";

    if (currentMode === 'signup') {
        // Run Signup API Call
        try {
            const response = await fetch('http://127.0.0.1:8000/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: usernameInput, password: passwordInput })
            });
            const data = await response.json();

            if (response.ok) {
                authMessage.innerText = "✅ Registration successful! Please Sign In.";
                authMessage.style.color = "#4ade80";
                tabLogin.click(); // Automatically bounce user over to login form page view
            } else {
                authMessage.innerText = `❌ ${data.detail || "Registration failed."}`;
                authMessage.style.color = "#ef4444";
            }
        } catch (err) {
            authMessage.innerText = "❌ Cannot connect to backend server.";
        }
    } else {
        // Run Login API Call (Updated to standard JSON payload format)
        try {
            const response = await fetch('http://127.0.0.1:8000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: usernameInput, password: passwordInput })
            });
            const data = await response.json();

            if (response.ok) {
                // Save digital signature credentials payload key
                localStorage.setItem('token', data.access_token);
                
                // Show console interface panel
                authScreen.classList.add('hidden');
                consoleScreen.classList.remove('hidden');
                authForm.reset();
            } else {
                // Fixed: handle both plain text detail or object detail strings
                authMessage.innerText = `❌ ${data.detail || "Invalid credentials."}`;
                authMessage.style.color = "#ef4444";
            }
        } catch (err) {
            authMessage.innerText = "❌ Connection failed.";
        }
    }
});

// --- LOG OUT ACTION ---
document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('token'); // Destroy saved keycard signature
    consoleScreen.classList.add('hidden');
    authScreen.classList.remove('hidden');
    authMessage.innerText = "Logged out securely.";
    authMessage.style.color = "#94a3b8";
});

// --- RUN AI SCAN ACTION ---
document.getElementById('scan-btn').addEventListener('click', async () => {
    const statusText = document.getElementById('status-text');
    const summarySection = document.getElementById('results-summary');
    const reportSection = document.getElementById('report-section');
    const container = document.getElementById('reports-container');
    const vulnCount = document.getElementById('vuln-count');

    statusText.innerText = "⏳ AI Engine auditing cloud configurations...";
    statusText.className = "status-scanning";
    
    try {
        const response = await fetch('http://127.0.0.1:8000/ai-analyze', { method: 'POST' });
        const data = await response.json();

        container.innerHTML = "";
        vulnCount.innerText = data.total_vulnerabilities;

        data.ai_analysis_report.forEach(item => {
            const card = document.createElement('div');
            card.className = 'ai-card';
            card.innerHTML = `
                <span class="severity-tag severity-${item.severity}">${item.severity}</span>
                <h3>${item.finding}</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">Resource ID: <code>${item.resource_id}</code></p>
                <p style="background-color: #0f172a; padding: 12px; border-radius: 6px; border-left: 3px solid #38bdf8;">
                    ${item.ai_remediation_advice}
                </p>
            `;
            container.appendChild(card);
        });

        statusText.innerText = "✅ Scan Complete. AI Report generated successfully!";
        statusText.className = "status-idle";
        summarySection.classList.remove('hidden');
        reportSection.classList.remove('hidden');

    } catch (error) {
        statusText.innerText = "❌ Error connecting to Backend Server.";
        statusText.className = "status-idle";
    }
});