from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="CloudGuard AI Backend")

# --- CROSS-ORIGIN RESOURCE SHARING (CORS) ---
# Allows your local frontend files to talk to the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "super-secret-cloudguard-key"
ALGORITHM = "HS256"

# In-memory user store for demo purposes
FAKE_USER_DB = {}

# --- DATA MODELS (SCHEMAS) ---
class UserAuth(BaseModel):
    username: str
    password: str

# --- HELPER FUNCTIONS ---
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- MOCK INFRASTRUCTURE DATA ---
def get_mock_data():
    return [
        {
            "id": "i-0abcd1234efgh5678",
            "type": "EC2 Instance",
            "name": "Production-Web-Server",
            "configuration": {"PortsOpen": "0.0.0.0/0"}
        },
        {
            "id": "arn:aws:s3:::company-financial-records-2026",
            "type": "S3 Bucket",
            "name": "company-financial-records-2026",
            "configuration": {"PublicAccess": True}
        }
    ]

# --- BACKEND BASE ROUTE ---
@app.get("/")
def home():
    return {"message": "CloudGuard AI Backend is Running!"}

# --- MODULE 1: AUTHENTICATION ENDPOINTS ---
@app.post("/signup")
def signup(user: UserAuth):
    if user.username in FAKE_USER_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already exists!"
        )
    FAKE_USER_DB[user.username] = {
        "username": user.username, 
        "password": hash_password(user.password)
    }
    return {"message": f"User {user.username} registered successfully!"}

@app.post("/login")
def login(user: UserAuth):
    db_user = FAKE_USER_DB.get(user.username)
    if not db_user or db_user["password"] != hash_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect username or password"
        )
    
    token = create_access_token(username=user.username)
    return {"access_token": token, "token_type": "bearer"}

# --- MODULE 2 & 3: AI ANALYSIS & RULE ENGINE ENDPOINT ---
@app.post("/ai-analyze")
def ai_analyze():
    """
    Simulates sending the cloud configuration metadata to an AI engine
    and receiving detailed security remediation steps.
    """
    resources = get_mock_data()
    ai_insights = []
    
    for resource in resources:
        if resource["type"] == "EC2 Instance" and resource["configuration"]["PortsOpen"] == "0.0.0.0/0":
            ai_insights.append({
                "resource_id": resource["id"],
                "severity": "CRITICAL",
                "finding": "SSH Port 22 open to the world.",
                "ai_remediation_advice": (
                    "AI Analysis: This setup exposes your instance to brute-force attacks. "
                    "Modify the AWS Security Group to restrict access to known corporate IP ranges only."
                )
            })
        elif resource["type"] == "S3 Bucket" and resource["configuration"]["PublicAccess"] == True:
            ai_insights.append({
                "resource_id": resource["id"],
                "severity": "HIGH",
                "finding": "S3 Bucket allows public read access.",
                "ai_remediation_advice": (
                    "AI Analysis: Confidential data might leak. Enable 'Block Public Access' "
                    "on this bucket immediately and use IAM Policies for access control."
                )
            })
            
    return {
        "status": "completed",
        "total_vulnerabilities": len(ai_insights),
        "ai_analysis_report": ai_insights
    }

# --- SERVER INITIATION ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)