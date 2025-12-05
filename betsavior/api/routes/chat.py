from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from betsavior.api.db import get_db
from betsavior.models.session import ChatMessage
from betsavior.utils.openai_client import ask_gpt

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    user_id: int = Field(..., description="Identifier of the user sending the message")
    message: str = Field(..., min_length=1, description="User message for the assistant")


class ChatResponse(BaseModel):
    response: str


def _build_history(messages: List[ChatMessage]) -> List[dict]:
    history: List[dict] = []
    for record in messages:
        history.append({"role": "user", "content": record.message})
        history.append({"role": "assistant", "content": record.response})
    return history


@router.post("", response_model=ChatResponse)
async def create_chat_message(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    history_records = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == payload.user_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    history = _build_history(history_records)

    try:
        response_text = ask_gpt(payload.message, history=history)
    except Exception as exc:  # pragma: no cover - external dependency
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    chat_record = ChatMessage(
        user_id=payload.user_id,
        message=payload.message,
        response=response_text,
    )
    db.add(chat_record)
    db.commit()
    db.refresh(chat_record)

    return ChatResponse(response=response_text)
