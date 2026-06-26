from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="CloudGuard AI Backend")

# --- CROSS-ORIGIN RESOURCE SHARING (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "super-secret-cloudguard-key"
ALGORITHM = "HS256"

# In-memory user store and findings database
FAKE_USER_DB = {}
FAKE_FINDINGS_DB = []  # <--- NEW: Stores processed security findings (Module 4)

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

# --- MODULE 2 & 3: MOCK INFRASTRUCTURE DATA ---
def get_mock_data():
    return [
        {
            "id": "i-0abcd1234efgh5678",
            "type": "EC2 Instance",
            "name": "Production-Web-Server",
            "configuration": {"PortsOpen": "0.0.0.0/0", "Encrypted": False}
        },
        {
            "id": "arn:aws:s3:::company-financial-records-2026",
            "type": "S3 Bucket",
            "name": "company-financial-records-2026",
            "configuration": {"PublicAccess": True, "SSEAlgorithm": None}
        },
        {
            "id": "arn:aws:iam::123456789012:role/AdminExecutionRole",
            "type": "IAM Role",
            "name": "AdminExecutionRole",
            "configuration": {"AttachedPolicies": ["AdministratorAccess"], "MissingEncryption": True}
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


# --- MODULE 4: RULE ENGINE EXTRACTION & API ---

def evaluate_security_rules(resource: dict) -> list:
    """Evaluates the resource against the Module 4 security rules."""
    findings = []
    r_type = resource["type"]
    config = resource.get("configuration", {})

    # Rule 1: Public S3 Bucket
    if r_type == "S3 Bucket" and config.get("PublicAccess") == True:
        findings.append({
            "resource_id": resource["id"],
            "resource_type": "S3",
            "rule_name": "public-bucket",
            "severity": "CRITICAL",
            "description": f"S3 Bucket '{resource['name']}' allows public read access.",
            "remediation": "Enable 'Block Public Access' on this bucket immediately."
        })

    # Rule 2: Open SSH Port
    if r_type == "EC2 Instance" and config.get("PortsOpen") == "0.0.0.0/0":
        findings.append({
            "resource_id": resource["id"],
            "resource_type": "EC2",
            "rule_name": "open-ssh-port",
            "severity": "HIGH",
            "description": f"EC2 Instance '{resource['name']}' has SSH port 22 open to the world.",
            "remediation": "Modify the AWS Security Group to restrict access to trusted IPs."
        })

    # Rule 3: AdminAccess Roles
    if r_type == "IAM Role" and "AdministratorAccess" in config.get("AttachedPolicies", []):
        findings.append({
            "resource_id": resource["id"],
            "resource_type": "IAM",
            "rule_name": "admin-access-role",
            "severity": "HIGH",
            "description": f"IAM Role '{resource['name']}' grants full AdministratorAccess.",
            "remediation": "Apply least-privilege scoping rules and remove broad administrator policies."
        })

    # Rule 4: Missing Encryption (Checks S3, EC2, or IAM contexts)
    if config.get("Encrypted") == False or config.get("SSEAlgorithm") is None or config.get("MissingEncryption") == True:
        findings.append({
            "resource_id": resource["id"],
            "resource_type": r_type.split()[0],
            "rule_name": "missing-encryption",
            "severity": "MEDIUM",
            "description": f"Resource '{resource['name']}' is missing server-side encryption configurations.",
            "remediation": "Enable default KMS or AES-256 encryption rules for this asset."
        })

    return findings


@app.post("/api/v1/compliance/scan")
def run_compliance_scan():
    """
    Module 4 Target: Discovers issues, stores them in the findings database,
    and reports execution state back.
    """
    global FAKE_FINDINGS_DB
    resources = get_mock_data()
    FAKE_FINDINGS_DB = [] # Reset data stream for fresh evaluation simulation
    
    for resource in resources:
        violations = evaluate_security_rules(resource)
        FAKE_FINDINGS_DB.extend(violations)
        
    return {
        "status": "success",
        "total_findings_logged": len(FAKE_FINDINGS_DB)
    }


@app.get("/api/v1/findings")
def get_findings():
    """Returns the logged security findings for Module 5 dashboard rendering."""
    return FAKE_FINDINGS_DB


# --- SERVER INITIATION ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)