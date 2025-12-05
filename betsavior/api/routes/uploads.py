from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from betsavior.api.db import get_db
from betsavior.models.upload import Upload
from betsavior.utils.ocr import extract_text

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("")
async def upload_image(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        contents = await file.read()
        processed_text = extract_text(contents)
    except Exception as exc:  # pragma: no cover - external dependency
        raise HTTPException(status_code=400, detail="Could not process image") from exc

    record = Upload(user_id=user_id, file_name=file.filename, processed_text=processed_text)
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"id": record.id, "processed_text": processed_text}
