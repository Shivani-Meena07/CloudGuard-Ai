from pydantic import BaseModel, Field
from datetime import datetime

class RemediationBase(BaseModel):
    aws_cli_command: str = Field(..., description="Executable AWS CLI script to remediate the vulnerability.")
    terraform_fix: str = Field(..., description="Terraform HCL block or modification showing the secure state.")
    best_practices: str = Field(..., description="Plain-English explanation of long-term prevention strategies.")

class RemediationCreate(RemediationBase):
    finding_id: int

class RemediationResponse(RemediationBase):
    id: int
    finding_id: int
    created_at: datetime

    class Config:
        from_attributes = True