from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Remediation(Base):
    __tablename__ = "remediations"

    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(Integer, ForeignKey("findings.id", ondelete="CASCADE"), unique=True, nullable=False)
    aws_cli_command = Column(Text, nullable=False)
    terraform_fix = Column(Text, nullable=False)
    best_practices = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to the finding
    finding = relationship("Finding", back_populates="remediation")
    