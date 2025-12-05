from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from betsavior.api.db import get_db
from betsavior.models.session import ChatMessage
from betsavior.models.upload import Upload
from betsavior.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/progress")
async def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    now = datetime.now(timezone.utc)
    created_at = user.created_at.replace(tzinfo=timezone.utc) if user.created_at else now
    days_without_betting = max((now - created_at).days, 0)

    messages_count = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).count()
    uploads_count = db.query(Upload).filter(Upload.user_id == user_id).count()

    return {
        "user_id": user_id,
        "email": user.email,
        "days_without_betting": days_without_betting,
        "messages_exchanged": messages_count,
        "uploads_processed": uploads_count,
    }
