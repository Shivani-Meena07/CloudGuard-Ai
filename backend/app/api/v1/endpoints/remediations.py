from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.remediation import RemediationResponse
from app.services.remediation_service import RemediationService

router = APIRouter(prefix="/remediations", tags=["Remediations"])

@router.post("/{finding_id}", response_model=RemediationResponse, status_code=status.HTTP_201_CREATED)
async def generate_remediation(finding_id: int, db: Session = Depends(get_db)):
    """
    Generate or retrieve actionable AWS CLI/Terraform remediation paths for a specific vulnerability finding.
    """
    service = RemediationService(db)
    try:
        remediation = await service.get_or_create_remediation(finding_id)
        return remediation
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))