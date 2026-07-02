import json
from sqlalchemy.orm import Session
from app.models.finding import Remediation, Finding
from app.schemas.remediation import RemediationCreate
# Import your LLM client initialized in Module 6 (e.g., from app.core.config or similar)
# For this example, we assume an OpenAI client or a LangChain/Bedrock implementation.

class RemediationService:
    def __init__(self, db_session: Session):
        self.db = db_session

    async def generate_remediation_from_ai(self, finding: Finding) -> dict:
        """
        Calls your LLM provider to get highly structured remediation code.
        """
        prompt = f"""
        You are an expert cloud security engineer and automated platform. 
        Generate a strict JSON response containing remediation instructions for the following AWS security finding:
        
        Resource Type: {finding.resource_type}
        Resource ID/ARN: {finding.resource_id}
        Vulnerability/Rule: {finding.rule_name}
        Severity: {finding.severity}
        Description: {finding.description}
        
        Provide the output in this EXACT JSON structure without markdown wrappers:
        {{
            "aws_cli_command": "# bash commands to fix it\\naws s3api ...",
            "terraform_fix": "# Terraform code\\nresource \\"aws_s3_bucket\\" ...",
            "best_practices": "Detailed markdown bullet points explaining prevention principles."
        }}
        """

        # --- Example Implementation using OpenAI Structured Output / JSON Mode ---
        # Modify this snippet to match your exact Module 6 LLM configuration
        try:
            # client = OpenAI()
            # response = client.chat.completions.create(
            #     model="gpt-4o",
            #     response_format={ "type": "json_object" },
            #     messages=[{"role": "user", "content": prompt}]
            # )
            # data = json.loads(response.choices[0].message.content)
            
            # Mock architecture fallback for demonstration:
            data = {
                "aws_cli_command": f"aws s3api put-public-access-block --bucket {finding.resource_id} --public-access-block-configuration 'BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true'",
                "terraform_fix": f"resource \"aws_s3_bucket_public_access_block\" \"example\" {{\n  bucket = \"{finding.resource_id}\"\n\n  block_public_acls       = true\n  block_public_policy     = true\n  ignore_public_acls      = true\n  restrict_public_buckets = true\n}}",
                "best_practices": "1. Implement Service Control Policies (SCPs) to deny modification of public access blocks.\n2. Enable AWS Config rules to monitor real-time drifting configurations.\n3. Implement the principle of least privilege using tight IAM resource statements."
            }
            return data
        except Exception as e:
            raise RuntimeError(f"Failed to generate remediation via LLM: {str(e)}")

    async def get_or_create_remediation(self, finding_id: int) -> Remediation:
        # Check if remediation already exists
        existing = self.db.query(Remediation).filter(Remediation.finding_id == finding_id).first()
        if existing:
            return existing

        # Fetch finding context
        finding = self.db.query(Finding).filter(Finding.id == finding_id).first()
        if not finding:
            raise ValueError("Finding not found")

        # Generate using AI
        raw_remediation = await self.generate_remediation_from_ai(finding)
        
        # Save to database
        db_remediation = Remediation(
            finding_id=finding_id,
            aws_cli_command=raw_remediation["aws_cli_command"],
            terraform_fix=raw_remediation["terraform_fix"],
            best_practices=raw_remediation["best_practices"]
        )
        self.db.add(db_remediation)
        self.db.commit()
        self.db.refresh(db_remediation)
        
        return db_remediation