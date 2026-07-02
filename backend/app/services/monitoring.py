import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal  # Adjust path to your DB session maker
from app.models.account import AWSAccount  # Model from Module 2
from app.services.scanner import run_aws_scan_pipeline  # Pipeline combining Module 3 & 4

logger = logging.getLogger("cloudguard.monitoring")

async def trigger_continuous_scan():
    """
    Background job that loops through all connected AWS accounts,
    discovers resources, runs the rule engine, and updates the DB.
    """
    logger.info("Continuous monitoring cycle started...")
    db: Session = SessionLocal()
    
    try:
        # Fetch only active/successfully verified accounts
        active_accounts = db.query(AWSAccount).filter(AWSAccount.is_active == True).all()
        
        if not active_accounts:
            logger.info("No active AWS accounts found to scan.")
            return

        for account in active_accounts:
            logger.info(f"Starting scheduled scan for Account: {account.account_id}")
            try:
                # This service function runs Module 3 (S3/EC2/IAM fetch) 
                # and Module 4 (Rule evaluation) then commits findings to DB.
                await run_aws_scan_pipeline(db=db, account=account)
                logger.info(f"Successfully completed scan for Account: {account.account_id}")
            except Exception as account_err:
                logger.error(f"Failed to scan account {account.account_id}: {str(account_err)}")
                continue  # Keep moving to next accounts even if one fails
                
    except Exception as e:
        logger.error(f"Critical failure during scheduled monitoring execution: {str(e)}")
    finally:
        db.close()